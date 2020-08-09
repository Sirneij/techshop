from django import forms
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from . import models
from django.contrib.auth.forms import UsernameField
from django.core.mail import send_mail
from django.contrib.auth import login, authenticate
import logging


logger = logging.getLogger(__name__)

class UserCreationForm(DjangoUserCreationForm):
    class Meta(DjangoUserCreationForm.Meta):
        model = models.User
        fields = ("email",)
        field_classes = {"email": UsernameField}

    def send_mail(self):
        logger.info(
            "Sending signup email for email=%s",
            self.cleaned_data["email"],
        )
        message = "Welcome {}".format(self.cleaned_data["email"])
        send_mail(
            "Welcome to Electro",
            message,
            "site@electro.domain",
            [self.cleaned_data["email"]],
            fail_silently=True,
        )


class AuthenticationForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'input100'}))
    password = forms.CharField(
        strip=False, widget=forms.PasswordInput(attrs={'class': 'input100'})
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email is not None and password:
            self.user = authenticate(
                self.request, email=email, password=password
            )
            login(self.request, self.user)
            if self.user is None:
                raise forms.ValidationError(
                    "Invalid email/password combination."
                )
            logger.info(
                "Authentication successful for email=%s", email
            )

        return self.cleaned_data

    def get_user(self):
        return self.user

class UserProfileForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'input', 'placeholder':'Email address'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Phone number', 'type':'tel'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'First name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Last name'}))
    shipping_address_1 = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'More preferred shipping address'}))
    shipping_address_2 = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Preferred shipping address'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Shipping City'}))
    shipping_zip = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Shipping address zip code'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Shipping country'}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'class':'input', 'placeholder':'Date of Birth'})) 
    phone_number =  forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Phone number', 'type':'tel'}))
    class Meta:
        model = models.UserProfile
        exclude = ('user',)
     