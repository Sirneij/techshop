from django.shortcuts import render, get_object_or_404
from . import cart
from django.template import RequestContext
from django.urls import reverse
from django.http import HttpResponseRedirect
from checkout import checkout, models
from techshop import settings

def cart_detail(request):
    """ view function for the page displaying the customer shopping cart, and allows for the updating of quantities
    and removal product instances 
    
    """
    if request.method == 'POST':
        postdata = request.POST.copy()
        if postdata['submit'] == '×':
            cart.remove_from_cart(request)
        if postdata['submit'] == 'Update':
            cart.update_cart(request)
        if postdata['submit'] == 'Checkout':
            return HttpResponseRedirect(reverse('checkout:checkout'))
    cart_items = cart.get_cart_items(request)
    page_title = 'Shopping Cart'
    cart_subtotal = cart.cart_subtotal(request)
    # need for Google Checkout button
    merchant_id = settings.AUTHNET_KEY
    return render(request, 'cart/detail.html', locals())
