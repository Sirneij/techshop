from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.http import HttpResponseRedirect

from .forms import CheckoutForm, OrderCreateForm
from .models import Order, OrderItem
from . import checkout
from cart import cart

from users import profile


def order_create(request):
    if request.method == 'POST':
        Order_form = OrderCreateForm(request.POST)
        if Order_form.is_valid():
            order = Order_form.save(commit=False)
            order.ip_address = checkout.get_client_ip(request)
            if request.user.is_authenticated:
                order.user = request.user
            cart_items = cart.get_cart_items(request)
            order.save()
            for item in cart_items:
                price = item.price
                product = item.product
                quantity = item.quantity
                OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)
            # clear the cart
            cart.empty_cart(request)
            # launch asynchronous task
            #order_created.delay(order.id)
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            order_items = OrderItem.objects.filter(order=order)
            return render(request, 'checkout/receipt.html', locals())
    else:
        if request.user.is_authenticated:
            user_profile = profile.retrieve(request)
            Order_form = OrderCreateForm(instance=user_profile)
        else:
            Order_form = OrderCreateForm()
    page_title = 'Checkout'
    return render(request, 'checkout/checkout.html', locals())