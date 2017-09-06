from rest_framework import generics, permissions
from . import models
from . import serializers


class ProductAPIView(generics.ListCreateAPIView,
                     generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Product.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    serializer_class = serializers.ProductSerializer


class ProductStockAPIView(generics.ListCreateAPIView,
                          generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProductStock.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    serializer_class = serializers.ProductStockSerializer


class ProductOrderAPIView(generics.ListCreateAPIView,
                          generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProductOrder.objects.all()
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = serializers.ProductOrderSerializer

    def perform_destroy(self, instance):
        quantity = instance.quantity
        product_stock = instance.product.stock
        product_stock.add_stock(quantity)
        instance.delete()


class TotalOrderAPIView(generics.ListCreateAPIView,
                        generics.RetrieveDestroyAPIView):
    queryset = models.TotalOrder.objects.all()
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = serializers.TotalOrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        serializer.instance.set_price()

    def perform_destroy(self, instance):
        instance.delete_product_orders()
        instance.delete()
