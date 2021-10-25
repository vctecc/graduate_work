from django.db import models


class Customer(models.Model):
    user_id = models.UUIDField()
    provider_customer_id = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'customers'

    def __str__(self):
        return f"User ID: {self.user_id},  ID from provider: {self.provider_customer_id}"


STATUS = (
    ('DRAFT', 'draft'),
    ('PROCESSING', 'processing'),
    ('PAID', 'paid'),
    ('ERROR', 'error'),
    ('CANCELED', 'canceled')
)


class Payment(models.Model):
    invoice_id = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, models.DO_NOTHING)
    status = models.CharField(max_length=255, choices=STATUS)
    product_id = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'payments'

    def __str__(self):
        tmpl = "[{}] Invoice: {} Customer: {} Product: {}"
        return tmpl.format(self.status, self.invoice_id, self.customer.user_id, self.product_id)
