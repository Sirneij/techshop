from .models import SearchTerm
from shop.models import Product
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.contrib.postgres.search import TrigramSimilarity
from stats import stats

STRIP_WORDS = ['a','an','and','by','for','from','in','no','not',
               'of','on','or','that','the','to','with']

def store(request, query):
    """ stores the search text """
    # if search term is at least three chars long, store in db
    if len(query) > 2:
        term = SearchTerm()
        term.query = query
        term.ip_address = request.META.get('REMOTE_ADDR')
        term.tracking_id = stats.tracking_id(request)
        term.user = None
        if request.user.is_authenticated:
            term.user = request.user
        term.save()
    
def products(search_text):
    """ get products matching the search text """
    words = _prepare_words(search_text)
    products = Product.objects.active()
    results = {}
    for word in words:
        search_vector = SearchVector('name', weight='A') + SearchVector('description', weight='B')+ SearchVector('product_specs', weight='B')+ SearchVector('meta_keywords', weight='C')
        search_query = SearchQuery(word)
        products = products.annotate(rank=SearchRank(search_vector, 
            search_query)).filter(rank__gte=0.1).order_by('-rank')
        # products = products.annotate(similarity=TrigramSimilarity('name', word)
        #     ,).filter(similarity__gt=0.1).order_by('-similarity')
        results['products'] = products
    return results
    
def _prepare_words(search_text):
    """ strip out common words, limit to 5 words """
    words = search_text.split()
    for common in STRIP_WORDS:
        if common in words:
            words.remove(common)
    return words[0:5]

