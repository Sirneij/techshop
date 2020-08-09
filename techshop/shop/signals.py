from . import models
from io import BytesIO
import logging
from PIL import Image
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver