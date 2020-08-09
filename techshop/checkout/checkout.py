from cart import cart
from .models import Order, OrderItem
from .forms import CheckoutForm
from . import authnet
from techshop import settings

from django.urls import reverse
import urllib

def get_client_ip(request):
    X_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if X_forwarded_for:
        ip = X_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip

def create_order(request, transaction_id):
    """ if the POST to the payment gateway successfully billed the customer, create a new order
    containing each CartItem instance, save the order with the transaction ID from the gateway,
    and empty the shopping cart
    
    """
    order = Order.objects.create()
    checkout_form = CheckoutForm(request.POST, instance=order)
    order = checkout_form.save(commit=False)
    
    order.transaction_id = transaction_id
    order.ip_address = get_client_ip()
    order.user = None
    if request.user.is_authenticated():
        order.user = request.user
    order.status = Order.SUBMITTED
    order.save()
    
    if order.pk:
        """ if the order save succeeded """
        cart_items = cart.get_cart_items(request)
        for ci in cart_items:
            """ create order item for each cart item """
            oi = OrderItem()
            oi.order = order
            oi.quantity = ci.quantity
            oi.price = ci.price  # now using @property
            oi.product = ci.product
            oi.save()
        # all set, clear the cart
        cart.empty_cart(request)
        
        # save profile info for future orders
        if request.user.is_authenticated():
            from .users import profile
            profile.set(request)
        
    return order
