from django.db import models

TRADE_TYPES = [
    ("BUY", "BUY"),
    ("SELL", "SELL"),
]
# Create your models here.
class Trade(models.Model):
    ticker = models.CharField(max_length=64)
    trade_type = models.CharField(max_length=64, choices=TRADE_TYPES)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()

class Portfolio(models.Model):
    ticker = models.CharField(max_length=64)
    average_buy_price = models.FloatField()
    quantity = models.PositiveIntegerField()
