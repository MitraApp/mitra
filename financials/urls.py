from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', views.get_auth, name='get_auth'),
    path('transactions/', views.get_transactions, name='get_transactions'),
    path('identity/', views.get_identity, name='get_identity'),
    path('balance/', views.get_balance, name='get_balance'),
    path('accounts/', views.get_accounts, name='get_accounts'),
    path('assets/', views.get_assets, name='get_assets'),
    path('holdings/', views.get_holdings, name='get_holdings'),
    path('investment_transactions/', views.get_investment_transactions, name='get_investment_transactions'),
    path('item/', views.item, name='item'),
    path('info/', views.info, name='info'),
]