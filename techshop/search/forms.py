from .models import SearchTerm
from django import forms

class SearchForm(forms.ModelForm):
	""" form class for accepting search terms """
	class Meta:
		model = SearchTerm
		fields = ('query',)
		
	def __init__(self, *args, **kwargs):
		super(SearchForm, self).__init__(*args, **kwargs)
		default_text = 'Search'
		self.fields['query'].widget.attrs['value'] = default_text
		self.fields['query'].widget.attrs['class'] = 'input'
		self.fields['query'].widget.attrs['onfocus'] = "if (this.value=='" + default_text + "')this.value = ''"
        
	include = ('query',)
