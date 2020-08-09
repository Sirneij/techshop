from .models import Product, ProductCategory, ProductReview
from django import forms
class ProductReviewForm(forms.ModelForm):
    """ Form class to submit a new ProductReview instance """
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Title of rating'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'input', 'placeholder':'Your Review'}))
    rating = forms.CharField(widget=forms.NumberInput(attrs={'class':'input', 'placeholder':'Choose from 1-5'}))
    class Meta:
        model = ProductReview
        exclude = ('user','product', 'is_approved')