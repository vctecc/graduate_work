import uuid

from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Product(BaseModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    period = models.IntegerField()
    price = models.IntegerField()
    currency_code = models.CharField(max_length=3, default='RUB')
    is_active = models.BooleanField(default=True, verbose_name='is active')

    class Meta:
        managed = False
        db_table = 'product'

    def __str__(self):
        if self.is_active:
            status = "ACTIVE"
        else:
            status = "INACTIVE"
        return f"[{status}] {self.name} for {self.period} days at the price of {self.price} {self.currency_code}"


STATES = (
    ('ACTIVE', 'active'),
    ('INACTIVE', 'inactive'),
    ('CANCELLED', 'cancelled')
)


class Subscription(BaseModel):
    user_id = models.UUIDField()
    product = models.ForeignKey(Product, models.DO_NOTHING)
    state = models.CharField(max_length=255, choices=STATES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'subscription'

    def __str__(self):
        return f"[{self.state}] User: {self.user_id} Product: {self.product.name}"
