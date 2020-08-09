from django import template
from decimal import *
from shop.models import Product
import locale

register = template.Library()

@register.filter(name='currency')
def currency(value):
    try:
        locale.setlocale(locale.LC_ALL,'en_US.UTF-8')
    except:
        locale.setlocale(locale.LC_ALL,'')
    loc = locale.localeconv()
    return locale.currency(value, loc['currency_symbol'], grouping=True)

@register.filter()
def multiply(price,val):
    old_price = price + (Decimal(price) * Decimal(val))
    formatted_price = format(old_price,".2f")
    return formatted_price

@register.filter()
def count_product(categories):
    return Product.objects.filter(categories=categories).count()

@register.filter()
def brand_count_product(brand):
    return Product.objects.filter(brand=brand).count()