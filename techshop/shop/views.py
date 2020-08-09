from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from .models import Product, ProductCategory, ProductBrand, ProductReview
from .forms import ProductReviewForm
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.core.cache import cache
from techshop.settings import CACHE_TIMEOUT
from cart import cart
from cart import forms
from stats import stats
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
# Create your views here.
def product_list(request):
    products = Product.objects.active()
    for product in products:
        categories = product.categories.filter(is_active=True)
    featured_products = Product.objects.featured()
    search_recs = stats.recommended_from_search(request)
    recently_viewed = stats.get_recently_viewed(request)
    view_recs = stats.recommended_from_views(request)
    top_seller = Product.objects.filter(is_bestseller=True)
    return render(request, 'shop/index.html', locals())


def product_detail(request, id, slug):
    cart_items = cart.get_cart_items(request)
    product_cache_key = request.path
    # try to get product from cache
    product = cache.get(product_cache_key)
    # if a cache miss, fall back on db query
    if not product:
        product = get_object_or_404(Product, id=id, slug=slug, active=True)
        # store item in cache for next time
        cache.set(product_cache_key, product, CACHE_TIMEOUT)
    categories = product.categories.filter(is_active=True)
    page_title = product.name
    meta_keywords = product.meta_keywords
    meta_description = product.meta_description
    # evaluate the HTTP method, change as needed
    review_form = ProductReviewForm(request.POST or None)
    if request.method == 'POST':
        #create the bound form
        postdata = request.POST.copy()
        add_to_cart_form = forms.ProductAddToCartForm(request, postdata)
        #check if posted data is valid
        if add_to_cart_form.is_valid():
            #add to cart and redirect to cart page
            cart.add_to_cart(request)
            # if test cookie worked, get rid of it
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            return HttpResponseRedirect(reverse("cart:cart_detail"))

        if review_form.is_valid():
            temp = review_form.save(commit=False)
            temp.product = product
            temp.user = request.user
            temp.save()
            return HttpResponseRedirect(product.get_absolute_url) 
    else:
        #create the unbound form. Notice the request as a keyword argument
        add_to_cart_form = forms.ProductAddToCartForm(request=request)
    # assign the hidden input the product slug
    add_to_cart_form.fields['product_slug'].widget.attrs['value'] = slug
    # set test cookie to make sure cookies are enabled
    request.session.set_test_cookie()
    all_category = ProductCategory.objects.all()
    stats.log_product_view(request, product)
    # product review additions, CH 10
    product_reviews = ProductReview.approved.filter(product=product).order_by('-date')
    if request.is_ajax():
        html = render_to_string('shop/product_review.html', locals(), request=request)
        return JsonResponse({'product': html})
    return render(request, 'shop/detail.html', locals())

def category_list(request, slug):
    c = get_object_or_404(ProductCategory, slug=slug)
    products = c.product_set.all()
    page_title = c.name
    meta_keywords = c.meta_keywords
    meta_description = c.meta_description 
    top_seller = Product.objects.filter(is_bestseller=True)
    return render(request, 'shop/category-shop.html', locals())

def brand_list(request, slug):
    pass
class StoreList(ListView):
    model = Product 
    template_name = "shop/store.html"
    paginate_by = 20
    def get_context_data(self,*args,**kwargs):
        request = self.request
        context = super(StoreList,self).get_context_data(*args,**kwargs)
        all_category = ProductCategory.objects.all()
        all_brand = ProductBrand.objects.all()
        all_product = Product.objects.filter(active=True)
        top_seller = Product.objects.filter(is_bestseller=True)
        context["all_category"] = all_category
        context["all_brand"] = all_brand
        context["all_product"] = all_product
        context['top_seller'] = top_seller
        return context