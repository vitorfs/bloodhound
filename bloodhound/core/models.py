from django.db import models

class Product(models.Model):
    NEW = u'NEW'
    OK = u'OK'
    ERROR = u'ERROR'
    NOT_FOUND = u'NOT_FOUND'

    PRODUCT_STATUS = (
        (NEW, u'New'),
        (OK, u'Ok'),
        (ERROR, u'Error'),
        (NOT_FOUND, u'Not found'),
        )

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    status = models.CharField(max_length=10, default=NEW, choices=PRODUCT_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    visited_at = models.DateTimeField(auto_now_add=True)

    current_price = models.FloatField(null=True)
    last_price = models.FloatField(null=True)
    price_raw_variance = models.FloatField(null=True)
    price_percentage_variance = models.FloatField(default=0.0)
    price_changes = models.IntegerField(default=0)

class PriceHistory(models.Model):
    product = models.ForeignKey(Product)
    price = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
