from django import forms
from shop.models import Product, ProductCategory


class ProductAddToCartForm(forms.Form):
    """ form class to add items to the shopping cart """
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'value':1, 'class':'input-number'}), 
                                  error_messages={'invalid':'Please enter a valid quantity.'}, 
                                  min_value=1)
    product_slug = forms.CharField(widget=forms.HiddenInput)
    
    def __init__(self, request=None, *args, **kwargs):
        """ override the default so we can set the request """
        self.request = request
        super(ProductAddToCartForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        """ custom validation to check for presence of cookies in customer's browser """
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError("Cookies must be enabled.")
        return self.cleaned_data

# class ProductReviewForm(forms.ModelForm):
#     """ Form class to submit a new ProductReview instance """
#     class Meta:
#         model = ProductReview
#         exclude = ('user','product', 'is_approved')
        
