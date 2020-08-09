from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart_id", "quantity", "date_added",)
    raw_id_fields = ("product",)

