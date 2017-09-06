from rest_framework import serializers
from .models import Product, ProductOrder, ProductStock, TotalOrder
from rest_framework.exceptions import ValidationError


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('pk', 'title', 'description', 'price',
                  'created_at', 'modified_at')


class ProductStockSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()

    class Meta:
        model = ProductStock
        fields = ['pk', 'product', 'stock']


class ProductOrderSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        product = validated_data.get('product')
        quantity = validated_data.get('quantity')
        product_stock = product.stock
        if not product_stock.is_available(quantity=quantity):
            msg = 'Not sufficient stock, available stock: {}'.format(
                product_stock.stock
            )
            raise ValidationError(msg)
        instance = self.Meta.model.objects.create(
            product=product, quantity=quantity
        )
        product_stock.remove_stock(quantity=quantity)
        return instance

    def update(self, instance, validated_data):
        product = validated_data.get('product', instance.product)
        prev_quantity = instance.quantity
        new_quantity = validated_data.get('quantity')
        product_stock = product.stock
        stock = product_stock.stock  # current stock

        # adding previous quantity to get the total stock
        total_stock = stock + prev_quantity

        if new_quantity > total_stock:
            msg = 'Not sufficient stock, available stock: {}'.format(stock)
            raise ValidationError(msg)

        instance.quantity = new_quantity
        total_stock -= new_quantity
        product_stock.stock = total_stock
        product_stock.save()
        instance.save()
        return instance

    class Meta:
        model = ProductOrder
        fields = ['pk', 'product', 'quantity']


class TotalOrderSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(read_only=True)

    user = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    product_orders = serializers.PrimaryKeyRelatedField(
        queryset=ProductOrder.objects.filter(total_order=None), many=True
    )

    total_price = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = TotalOrder
        fields = ('pk', 'user', 'product_orders', 'total_price', 'status')
