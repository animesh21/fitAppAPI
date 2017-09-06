from django.contrib import admin
from .models import Product, ProductStock, TotalOrder

# Register your models here.
admin.site.register((Product, ProductStock, TotalOrder))
