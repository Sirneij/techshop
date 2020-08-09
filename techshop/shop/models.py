from django.db import models

# Create your models here.

import os
import random
from django.db.models import Q
from django.urls import reverse
from PIL import Image
from techshop import settings


def get_image_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext 

def upload_image_path(instance,filename):
    name, ext = get_image_ext(filename)
    new_filename = random.randint(1,3910209312)
    final_filename = "{new_filename}{ext}".format(
                        new_filename = new_filename,
                        ext = ext
                    )
    return "product/{new_filename}/{final_filename}".format(
                        new_filename = new_filename,
                        final_filename = final_filename
                    )
class ProductManager(models.Manager):

    def featured(self):
        return self.get_queryset().filter(
                    featured=True,
                    active = True,
                )[:3]

    def latest_arival(self):
        return self.get_queryset().filter(
                        latest_arri=True,
                        active = True,
                    )[:3]

    def special_offer(self):
        return self.get_queryset().filter(
                        special_offer = True,
                        active = True,
                    )[:10]
    
    def special_deal(self):
        return self.get_queryset().filter(
                        special_deal = True,
                        active = True,
                    )[:5]
    def active(self):
        return self.get_queryset().filter(
                        active = True,
                    )

    def search(self,query):
        lookup = (
                    Q(title__icontains=query) | 
                    Q(description__icontains=query) |
                    Q(producttag__title__icontains=query)
                )
        return self.get_queryset().filter(lookup).distinct()
class ActiveCategoryManager(models.Manager):
    """ Manager class to return only those categories where each instance is active """
    def get_query_set(self):
        return super(ActiveCategoryManager, self).get_query_set().filter(is_active=True)

class ProductCategory(models.Model):
    name           = models.CharField(max_length=250)
    slug            = models.SlugField(unique=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField(max_length=255,
                                     help_text='Comma-delimited set of SEO keywords for keywords meta tag')
    meta_description = models.CharField(max_length=255,
                                        help_text='Content for description meta tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ActiveCategoryManager()

    class Meta:
        ordering = ('name',)
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("shop:product_list_by_category", kwargs={"slug":self.slug})
    @property
    def cache_key(self):
        return self.get_absolute_url()

class ProductTagManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class ProductTag(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(max_length=48)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    objects = ProductTagManager()

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.slug,)

class ProductBrand(models.Model):
    name           = models.CharField(max_length=250)
    slug            = models.SlugField(unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return str(self.name)

    @property
    def get_absolute_url(self):
        return reverse("shop:product_list_by_brand",kwargs={"slug":self.slug})

class Product(models.Model):
    name = models.CharField(max_length=400, db_index=True)
    categories = models.ManyToManyField(ProductCategory) 
    brand = models.ForeignKey(ProductBrand,on_delete=models.CASCADE, blank=True, related_name='products')
    description = models.TextField(blank=True)
    product_specs = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=9,decimal_places=2)
    old_price = models.DecimalField(max_digits=9,decimal_places=2, blank=True,default=0.00)
    slug = models.SlugField(max_length=2000, db_index=True)
    tags = models.ManyToManyField(ProductTag, blank=True)
    active = models.BooleanField(default=True)
    main_image   = models.ImageField(upload_to = upload_image_path, null = True, blank = True,)
    in_stock = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    featured        = models.BooleanField(default=False)
    latest_arri          = models.BooleanField(default=False)
    special_offer   = models.BooleanField(default=False)
    special_deal    = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    meta_keywords = models.CharField("Meta Keywords",max_length=255,
                                     help_text='Comma-delimited set of SEO keywords for keywords meta tag')
    meta_description = models.CharField("Meta Description", max_length=255,
                                        help_text='Content for description meta tag')
    objects = ProductManager()
    class Meta:
        ordering = ('-id',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    @property
    def get_absolute_url(self):
        return reverse("shop:product_detail",kwargs={"id":self.id, "slug":self.slug})

    @property
    def sale_price(self):
        if self.old_price > self.price:
            return self.price
        else:
            return None
    @property
    def get_discount_percent(self):
        if self.old_price > self.price:
            discount = ((self.old_price - self.price)/self.old_price)*100
            discount = format(discount,".0f")
            return discount
    def cross_sells(self):
        """ gets other Product instances that have been combined with the current instance in past orders. Includes the orders
        that have been placed by anonymous users that haven't registered
        """
        from checkout.models import Order, OrderItem
        orders = Order.objects.filter(orderitem__product=self)
        order_items = OrderItem.objects.filter(order__in=orders).exclude(product=self)
        products = Product.active.filter(orderitem__in=order_items).distinct()
        return products
    
    # users who purchased this product also bought....
    def cross_sells_user(self):
        """ gets other Product instances that have been ordered by other registered customers who also ordered the current
        instance. Uses all past orders of each registered customer and not just the order in which the current 
        instance was purchased
        
        """
        from checkout.models import Order, OrderItem
        from users import models
        users = models.User.objects.filter(order__orderitem__product=self)
        items = OrderItem.objects.filter(order__user__in=users).exclude(product=self)
        products = Product.active.filter(orderitem__in=items).distinct()
        return products
    
    def cross_sells_hybrid(self):
        """ gets other Product instances that have been both been combined with the current instance in orders placed by 
        unregistered customers, and all products that have ever been ordered by registered customers
        
        """
        from checkout.models import Order, OrderItem
        from django.db.models import Q
        from users import models
        orders = Order.objects.filter(orderitem__product=self)
        users = models.User.objects.filter(order__orderitem__product=self)
        items = OrderItem.objects.filter( Q(order__in=orders) | 
                      Q(order__user__in=users) 
                      ).exclude(product=self)
        products = Product.objects.filter(orderitem__in=items, active=True).distinct()
        return products
    @property
    def cache_key(self):
        return self.get_absolute_url()

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = upload_image_path)
    thumbnail = models.ImageField(upload_to="product-thumbnails", null=True)

class ActiveProductReviewManager(models.Manager):
    """ Manager class to return only those product reviews where each instance is approved """
    def all(self):
        return super(ActiveProductReviewManager, self).all().filter(is_approved=True)
        
class ProductReview(models.Model):
    """ model class containing product review data associated with a product instance """
    RATINGS = ((5,5),(4,4),(3,3),(2,2),(1,1),)
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveSmallIntegerField(default=5, choices=RATINGS)
    is_approved = models.BooleanField(default=True)
    content = models.TextField()
    
    objects = models.Manager()
    approved = ActiveProductReviewManager()
    