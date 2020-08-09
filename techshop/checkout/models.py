from django.db import models

# Create your models here.
from django import forms
from shop.models import Product
from techshop import settings
import decimal
from django.urls import reverse

# class Country(models.Model):
#     name = models.CharField(max_length=30)

#     def __str__(self):
#         return self.name


# class City(models.Model):
#     country = models.ForeignKey(Country, on_delete=models.CASCADE)
#     name = models.CharField(max_length=30)

#     def __str__(self):
#         return self.name

class BaseOrderInfo(models.Model):
    """ base class for storing customer order information """
    class Meta:
        abstract = True
        
    #contact info
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=20)
    
    #shipping information
    shipping_address_1 = models.CharField(max_length=50)
    shipping_address_2 = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    shipping_zip = models.CharField(max_length=20)
    
    #billing information
    # billing_name = models.CharField(max_length=50)
    # billing_address_1 = models.CharField(max_length=50)
    # billing_address_2 = models.CharField(max_length=50, blank=True)
    # billing_city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    # billing_country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    # billing_zip = models.CharField(max_length=10)

class Order(BaseOrderInfo):
    """ model class for storing a customer order instance """
    # each individual status
    SUBMITTED = 1
    PROCESSED = 2
    SHIPPED = 3
    CANCELLED = 4
    # set of possible order statuses
    ORDER_STATUSES = ((SUBMITTED,'Submitted'),
                      (PROCESSED,'Processed'),
                      (SHIPPED,'Shipped'),
                      (CANCELLED,'Cancelled'),)
    #order info
    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=ORDER_STATUSES, default=SUBMITTED)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    braintree_id = models.CharField(max_length=150, blank=True)
    
    def __str__(self):
        return 'Order {}'.format(str(self.id))
    
    def get_total_cost(self):
        total = decimal.Decimal('0.00')
        order_items = OrderItem.objects.filter(order=self)
        for item in order_items:
            total += item.get_cost()
        return total

    def get_absolute_url(self):
        return reverse("users:order_details", kwargs={"id":self.id})
    
class OrderItem(models.Model):
    """ model class for storing each Product instance purchased in each order """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=9,decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    
    def get_cost(self):
        return self.price * self.quantity
    
    @property
    def name(self):
        return self.product.name
    
    
    def __str__(self):
        return self.product.name 
   