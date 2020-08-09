from django import forms
from .models import Order
from techshop.settings import DEBUG
import datetime
import re


class OrderCreateForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'input', 'placeholder':'Email address'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Phone number', 'type':'tel'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'First name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Last name'}))
    shipping_address_1 = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'More preferred shipping address'}))
    shipping_address_2 = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Preferred shipping address'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Shipping City'}))
    shipping_zip = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Shipping address zip code'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Shipping country'}))
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'shipping_address_1', 'shipping_address_2',
                  'shipping_zip', 'city', 'country',]



def cc_expire_years():
    """ list of years starting with current twelve years into the future """
    current_year = datetime.datetime.now().year
    years = range(current_year, current_year+12)
    return [(str(x),str(x)) for x in years]

def cc_expire_months():
    """ list of tuples containing months of the year for use in credit card form.
    [('01','January'), ('02','February'), ... ]
    
    """
    months = []
    for month in range(1,13):
        if len(str(month)) == 1:
            numeric = '0' + str(month)
        else:
            numeric = str(month)
        months.append((numeric, datetime.date(2009, month, 1).strftime('%B')))
    return months

CARD_TYPES = (('Mastercard','Mastercard'),
             ('VISA','VISA'),
             ('AMEX','AMEX'),
             ('Discover','Discover'),)
def strip_non_numbers(data):
    """ gets rid of all non-number characters """
    non_numbers = re.compile('\D')
    return non_numbers.sub('', data)
    

def cardLuhnChecksumIsValid(card_number):
    """ checks to make sure that the card passes a Luhn mod-10 checksum 
    Taken from: http://code.activestate.com/recipes/172845/
    
    """
    sum = 0
    num_digits = len(card_number)
    oddeven = num_digits & 1
    for count in range(0, num_digits):
        digit = int(card_number[count])
        if not (( count & 1 ) ^ oddeven ):
            digit = digit * 2
        if digit > 9:
            digit = digit - 9
        sum = sum + digit
    return ( (sum % 10) == 0 )

class CheckoutForm(forms.ModelForm):
    """ checkout form class to collect user billing and shipping information for placing an order """
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'input', 'placeholder':'Email address'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Phone number', 'type':'tel'}))
    shipping_name = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Shipping name'}))
    shipping_address_1 = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'More preferred shipping address'}))
    shipping_address_2 = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Preferred shipping address'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Shipping City'}))
    shipping_zip = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Shipping address zip code'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'class':'country_to_state country_select', 'placeholder':'Select shipping country'}))
    credit_card_number = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Card number'}))
    credit_card_type = forms.CharField(widget=forms.Select(choices=CARD_TYPES, attrs={'class':'input-select', 'placeholder':'Select card type'}))
    credit_card_expire_month = forms.CharField(widget=forms.Select(choices=cc_expire_months(), attrs={'class':'input-select' , 'placeholder':'Select card expiry month'}))
    credit_card_expire_year = forms.CharField(widget=forms.Select(choices=cc_expire_years(), attrs={'class':'input-select', 'placeholder':'Select card expiry year'}))
    credit_card_cvv = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Enter card cvv'}))
        
    class Meta:
        model = Order
        exclude = ('status','ip_address','user','transaction_id',)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_credit_card_number(self):
        """ validate credit card number if valid per Luhn algorithm """
        cc_number = self.cleaned_data['credit_card_number']
        stripped_cc_number = strip_non_numbers(cc_number)
        if not cardLuhnChecksumIsValid(stripped_cc_number):
            raise forms.ValidationError('The credit card you entered is invalid.')
        
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        stripped_phone = strip_non_numbers(phone)
        if len(stripped_phone) < 10:
            raise forms.ValidationError('Enter a valid phone number with area code.(e.g. 555-555-5555)')
        return self.cleaned_data['phone']