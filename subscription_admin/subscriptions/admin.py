from django.contrib import admin
from import_export.admin import ExportMixin

from .models import Subscription, Product


class ExportAdmin(ExportMixin, admin.ModelAdmin):
    pass


@admin.register(Subscription)
class SubscriptionAdmin(ExportAdmin):
    list_filter = ('state', 'product__name', 'start_date', 'end_date', )
    search_fields = ['product__id', 'product__name', 'user_id']


@admin.register(Product)
class ProductAdmin(ExportAdmin):
    list_filter = ('name', 'is_active')
    search_fields = ['name', 'is_active', 'price', 'period']
