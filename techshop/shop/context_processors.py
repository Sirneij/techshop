from techshop import settings
from shop.models import ProductCategory, ProductBrand
from cart import cart
from users.models import UserProfile
from search.forms import SearchForm

def techshop(request):
    """ context processor for the site templates """
    cart_item_count = cart.cart_distinct_item_count(request)
    query = request.GET.get('query','')
    form = SearchForm({'query': query })
    return {
    		'all_category': ProductCategory.objects.filter(is_active=True),
    		'all_brand': ProductBrand.objects.all(),
            'site_name': settings.SITE_NAME,
            'meta_keywords': settings.META_KEYWORDS,
            'meta_description': settings.META_DESCRIPTION,
            'analytics_tracking_id': settings.ANALYTICS_TRACKING_ID,
            'request': request,
            'cart_items': cart.get_cart_items(request),
            'cart_item_count': cart_item_count,
            'cart_subtotal':cart.cart_subtotal(request),
            'form': form
            }
