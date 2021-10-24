from django.contrib import admin

from .models import Subscription, Product


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_filter = ('state', 'product__name', 'start_date', 'end_date', )
    search_fields = ['product__id', 'product__name', 'user_id']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = ('name', 'is_active')
    search_fields = ['name', 'is_active', 'price', 'period']

