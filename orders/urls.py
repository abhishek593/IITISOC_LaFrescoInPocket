from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('confirm_place_order/', views.confirm_place_order, name='confirm_place_order'),
    path('all_orders/', views.all_orders, name='all_orders'),
]
