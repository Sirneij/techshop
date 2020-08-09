from django.db import models

# Create your models here.
from techshop import settings

class SearchTerm(models.Model):
    """ stores the text of each internal search submitted """
    query = models.CharField(max_length=2000)
    search_date = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    tracking_id = models.CharField(max_length=50, default='')
    
    def __str__(self):
        return self.query
