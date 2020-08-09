from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import login, authenticate
import logging
from . import forms, models
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from checkout.models import Order, OrderItem
from .forms import UserProfileForm
from . import profile
from .models import UserProfile

logger = logging.getLogger(__name__)

class SignupView(FormView):
    template_name = "users/signup.html"
    form_class = forms.UserCreationForm

    def get_success_url(self):
        redirect_to = self.request.GET.get("next", "/")
        return redirect_to

    def form_valid(self, form):
        response = super().form_valid(form)
        form.save()

        email = form.cleaned_data.get("email")
        raw_password = form.cleaned_data.get("password1")
        logger.info(
            "New signup for email=%s through SignupView", email
        )

        user = authenticate(email=email, password=raw_password)
        models.UserProfile.objects.create(user=user)
        login(self.request, user)

        form.send_mail()

        messages.info(
            self.request, "You signed up successfully."
        )

        return response

@login_required
def my_account(request, id):
    """ page displaying customer account information, past order list and account options """
    page_title = 'My Account'
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if profile_form.is_valid():
            user = profile_form.save(commit=False)
            user.save()
            messages.success(request, 'Profile updated successfully')
            return redirect(user.get_account_absolute_url())
        else:
            messages.error(request, 'Error updating your profile')
    else:
        profile_form = UserProfileForm(instance=request.user.userprofile)
    orders = Order.objects.filter(user=request.user)
    return render(request, "users/my_account.html", locals())

@login_required
def order_details(request, id):
    """ displays the details of a past customer order; order details can only be loaded by the same 
    user to whom the order instance belongs.
    
    """
    order = get_object_or_404(Order, id=id, user=request.user)
    page_title = 'Order Details for Order #' + str(id)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, "users/order_details.html", locals())

@login_required
def order_info(request):
    """ page containing a form that allows a customer to edit their billing and shipping information that
    will be displayed in the order form next time they are logged in and go to check out """
    if request.method == 'POST':
        postdata = request.POST.copy()
        user_form = UserProfileForm(postdata)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user = profile.retrieve(request)
            user.save()
            return redirect(user.get_account_absolute_url())
    else:
        user_profile = profile.retrieve(request)
        user_form = UserProfileForm(instance=user_profile)
    page_title = 'Edit Order Information'
    #order_items = OrderItem.objects.filter(id=id)
    return render(request, 'users/order_info.html', locals())
    

# def load_cities(request):
#     country_id = request.GET.get('shipping_country')
#     cities = City.objects.filter(country_id=country_id).order_by('name')
#     return render(request, 'users/city_dropdown_list_options.html', {'cities': cities})

