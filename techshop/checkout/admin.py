from django.contrib import admin

# Register your models here.
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__','date','status', 'user', 'paid')
    list_filter = ('paid', 'status','date')
    search_fields = ('email','shipping_name', 'id',)
    inlines = [OrderItemInline]
    
    fieldsets = (
                 ('Basics', {'fields': ('status','email','phone', 'first_name', 'last_name')}),
                 ('Shipping', {'fields':('shipping_address_1',
                'shipping_address_2','city','shipping_zip','country')}),
                 )