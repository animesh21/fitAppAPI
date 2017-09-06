from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(null=True, default=None)

    def __str__(self):
        return self.title


class ProductStock(models.Model):
    product = models.OneToOneField(Product, related_name='stock')
    stock = models.IntegerField(default=0)

    def is_available(self, quantity):
        return self.stock >= quantity

    def remove_stock(self, quantity):
        self.stock -= quantity
        self.save()

    def add_stock(self, quantity):
        self.stock += quantity
        self.save()

    def __str__(self):
        return '<{}: {}>'.format(self.product.title, self.stock)


class ProductOrder(models.Model):
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=0)
    total_order = models.ForeignKey(
        'TotalOrder', null=True, default=None,
        related_name='product_orders'
    )

    def add_to_stock_and_delete(self):
        self.product.stock.add_stock(self.quantity)
        self.delete()

    def __str__(self):
        return '<{}: {}>'.format(self.product.title, self.quantity)


class TotalOrder(models.Model):

    INITIATED = 'Init'
    COMPLETED = 'Comp'
    DELIVERED = 'Deli'
    CANCELLED = 'Canc'

    ORDER_STATUS_CHOICES = (
        (INITIATED, 'Initiated'),
        (COMPLETED, 'Completed'),
        (DELIVERED, 'Delivered'),
        (CANCELLED, 'Cancelled')
    )

    user = models.ForeignKey(User)
    total_price = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=4, choices=ORDER_STATUS_CHOICES,
                              default=INITIATED)

    def set_price(self):
        from django.db.models import F, Sum
        total = self.product_orders.values(
            'product__price', 'quantity'
        ).aggregate(sum=Sum(F('product__price') * F('quantity')))
        self.total_price = total['sum']
        self.status = self.COMPLETED
        self.save()
        return self.total_price

    def delete_product_orders(self):
        for product_order in self.product_orders.all():
            product_order.add_to_stock_and_delete()

    def __str__(self):
        return '<id: {}>'.format(self.id)
