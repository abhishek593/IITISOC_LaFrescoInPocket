from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('list_items/', views.list_items, name='list_items'),
    path('add_item/', views.add_item, name='add_item'),
    path('show_cart/', views.show_cart, name='show_cart'),
    path('remove_item/', views.remove_item, name='remove_item'),
]
