from django.urls import path

from . import views

app_name = 'register'

urlpatterns = [
    path('', views.register, name='register'),
    path('link_plaid/', views.link_plaid, name='link_plaid'),
    path('get_link_token/', views.get_link_token, name='get_link_token'),
    path('get_access_token/', views.get_access_token, name='get_access_token'),

]
