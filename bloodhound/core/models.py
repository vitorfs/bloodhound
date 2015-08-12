# coding: utf-8

from django.db import models
from django.utils import timezone


def format_currency(price):
    formatted_price = u''
    if price:
        try:
            formatted_price = u'{:,.2f} €'.format(price).replace(',', ' ').replace('.', ',')
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

    name = models.CharField(max_length=500, null=True, blank=True)
    code = models.CharField(max_length=255, unique=True)
    manufacturer = models.CharField(max_length=255, null=True)
    manufacturer_code = models.CharField(max_length=255, null=True)
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
            if self.current_price and self.last_price:
                self.price_raw_variance = self.current_price - self.last_price
                if self.current_price > 0 and self.last_price > 0:
                    if self.last_price < self.current_price:
                        self.price_percentage_variance = self.last_price / self.current_price
                        self.price_percentage_variance = 1.0 - self.price_percentage_variance
                    elif self.last_price > self.current_price:
                        self.price_percentage_variance = self.current_price / self.last_price
                        self.price_percentage_variance = self.price_percentage_variance - 1.0
                else:
                    self.price_percentage_variance = 0.0
            else:
                self.price_raw_variance = None
                self.price_percentage_variance = 0.0
            self.price_changes = self.price_history.count()
            self.status = self.OK
            self.updated_at = timezone.now()
            self.save()
            PriceHistory(product=self, price=price).save()

    def get_current_price_display(self):
        return format_currency(self.current_price)

    def get_price_raw_variance_display(self):
        value = self.price_raw_variance
        if value < 0:
            value = value * -1        
        return format_currency(value)

    def get_price_percentage_variance_display(self):
        value = self.price_percentage_variance * 100
        if value < 0:
            value = value * -1
        return u'{:.2f}%'.format(value)

    def get_url(self):
        if not self.url:
            self.url = u'http://www.verkkokauppa.com/fi/product/{0}'.format(self.code)
        return self.url

class PriceHistory(models.Model):
    product = models.ForeignKey(Product, related_name='price_history')
    price = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def get_price_display(self):
        return format_currency(self.price)

class Image(models.Model):
    product = models.ForeignKey(Product, related_name='images')
    url = models.URLField(max_length=1000)

    def get_secure_url(self):
        return self.url.replace('http://', 'https://')
