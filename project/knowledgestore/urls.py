"""application urls"""
from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    #authentification
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    #app urls
    path('panier/<int:id>/', views.panier, name='panier'),
    path('shop/', views.shop, name='shop'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('search/', views.shop, name='search'),
    path('ajouter_au_panier/<int:item_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('supprimer_du_panier/<int:item_id>/', views.supprimer_du_panier, name='supprimer_du_panier'),
    path('pass_commande/<int:item_id>/', views.pass_commande, name='pass_commande'),
    path('supprimer_du_commande/<int:item_id>/', views.supprimer_du_commande, name='supprimer_du_commande'),
    path('commande/<int:id>/', views.commande, name='commande'),
    path('adresse/<int:item_id>/', views.adresse, name='adresse'),
    path('saved-addresses/', views.saved_addresses, name='saved_addresses'),
    path('add-address/', views.add_address, name='add_address'),
    path('edit-address/', views.edit_address, name='edit_address'),
    path('delete-address/', views.delete_address, name='delete_address'),
    path('order-history/', views.order_history, name='order_history'),
    path('authors/', views.authors, name='authors'),
    path('authors/<str:author_name>/', views.author_books, name='author_books'),
]
