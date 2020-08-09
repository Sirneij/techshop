from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path("", views.product_list, name='index'),
    path('category/<slug:slug>/list/', views.category_list,name="product_list_by_category"),
    path('store/', views.StoreList.as_view(),name="product_store"),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    # path('review/product/add/', views.add_review, name='add_review'), 
]