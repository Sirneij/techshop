from django.shortcuts import render
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from . import search
from techshop import settings

#from django.utils import simplejson
from django.http import HttpResponse
from django.core import serializers
from shop.models import Product

def results(request):
    """ template for displaying settings.PRODUCTS_PER_PAGE paginated product results """
    # get current search phrase
    query = request.GET.get('query', '')
    # get current page number. Set to 1 is missing or invalid
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1
        
    matching = search.products(query).get('products', [])
    # generate the pagintor object
    paginator = Paginator(matching, 
                          settings.PRODUCTS_PER_PAGE)
    try:
        results = paginator.page(page).object_list
    except (InvalidPage, EmptyPage):
        results = paginator.page(1).object_list
        
    search.store(request, query)
    
    page_title = 'Search Results for: ' + query
    return render(request, 'search/results.html', locals())
