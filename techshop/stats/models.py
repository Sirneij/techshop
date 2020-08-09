from django.db import models

# Create your models here.
from techshop import settings
from shop.models import Product

class PageView(models.Model):
    """ model class for tracking the pages that a customer views """
    class Meta:
        abstract = True
        
    date = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT)
    tracking_id = models.CharField(max_length=50, default='', db_index=True)

class ProductView(PageView):
    """ tracks product pages that customer views """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
