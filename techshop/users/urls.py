from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from . import views, forms

app_name = "users"
urlpatterns = [
    path("login/", LoginView.as_view(
    	template_name="users/signin.html",form_class=forms.AuthenticationForm,), name="login",),
    path('logout/', LogoutView.as_view(), name="logout"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("account/<int:id>/", views.my_account, name="user_account"),
    path("orderinfo/", views.order_info, name="order_info"),
    path("<int:id>/orderdetail/", views.order_details, name="order_details"),
    #path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
]