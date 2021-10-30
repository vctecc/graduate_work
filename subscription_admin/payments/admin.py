from django.contrib import admin
from import_export.admin import ExportMixin

from .models import Customer, Payment


class MultiDBModelAdmin(ExportMixin, admin.ModelAdmin):
    # A handy constant for the name of the alternate database.
    using = 'payments'

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


@admin.register(Customer)
class CustomerAdmin(MultiDBModelAdmin):
    search_fields = ['user_id', 'provider_customer_id']
    list_filter = ('user_id', 'provider_customer_id')


@admin.register(Payment)
class PaymentAdmin(MultiDBModelAdmin):
    list_filter = ('status', )
    search_fields = ['invoice_id', 'customer__user_id', 'customer__provider_customer_id', 'product_id', 'status']
