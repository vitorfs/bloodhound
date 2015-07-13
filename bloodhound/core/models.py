# coding: utf-8

from django.db import models

def format_price(price):
    formatted_price = u''
    if price:
        try:
            formatted_price = u'{:.2f} €'.format(price)
        except:
            pass
    return formatted_price

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

    name = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=255, unique=True)
    url = models.URLField(max_length=1000, null=True, blank=True)
    status = models.CharField(max_length=10, choices=PRODUCT_STATUS, default=NEW)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    visited_at = models.DateTimeField(auto_now=True)

    current_price = models.FloatField(null=True)
    last_price = models.FloatField(null=True)
    price_raw_variance = models.FloatField(null=True)
    price_percentage_variance = models.FloatField(default=0.0)
    price_changes = models.IntegerField(default=0)

    def update_price(self, price):
        if price != self.current_price:
            self.last_price = self.current_price
            self.current_price = price
            self.price_changes = self.price_history.count()
            self.status = self.OK
            self.save()
            PriceHistory(product=self, price=price).save()

    def get_current_price_display(self):
        return format_price(self.current_price)

class PriceHistory(models.Model):
    product = models.ForeignKey(Product, related_name='price_history')
    price = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
