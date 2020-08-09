from django.db import models 
from django.contrib.auth.models import AbstractUser, BaseUserManager
from checkout.models import BaseOrderInfo
from django.core.validators import RegexValidator
from django.conf import settings

from django.urls import reverse

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                "Superuser must have is_staff=True."
            )
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser must have is_superuser=True."
            )

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField("email address", unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def is_employee(self):
        return self.is_active and (
            self.is_superuser
            or self.is_staff
            and self.groups.filter(name="Employees").exists()
        )

    @property
    def is_dispatcher(self):
        return self.is_active and (
            self.is_superuser
            or self.is_staff
            and self.groups.filter(name="Dispatchers").exists()
        )
import os
import random

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
    return "user/{new_filename}/{final_filename}".format(
                        new_filename = new_filename,
                        final_filename = final_filename
                    )
class UserProfile(BaseOrderInfo):
    """ stores customer order information used with the last order placed; can be attached to the checkout order form
    as a convenience to registered customers who have placed an order in the past.
    
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_pics =models.ImageField(upload_to = upload_image_path, null = True, blank = True,)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+\d*$', message="Phone number must be entered in the format: '+999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=20, blank=True)
    
    def __str__(self):
        return 'User Profile for: ' + self.user.email

    def get_account_absolute_url(self):
        return reverse("users:user_account", kwargs={"id":self.id})
