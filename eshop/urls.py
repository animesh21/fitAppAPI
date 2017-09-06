from django.conf.urls import url
from eshop import views

urlpatterns = [
    url(r'^products/(?P<pk>[0-9]*)$',
        views.ProductAPIView.as_view(),
        name='product'),
    url(r'^product-stocks/(?P<pk>[0-9]*)$',
        views.ProductStockAPIView.as_view(),
        name='product-stock'),
    url(r'^product-orders/(?P<pk>[0-9]*)$',
        views.ProductOrderAPIView.as_view(),
        name='product-order'),
    url(r'^total-orders/(?P<pk>[0-9]*)$',
        views.TotalOrderAPIView.as_view(),
        name='total-order')
]
