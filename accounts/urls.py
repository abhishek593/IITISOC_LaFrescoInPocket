from django.urls import path

from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('confirm_registration/<str:uidb64>/<str:token>/', views.confirm_register_user, name='confirm_registration'),
    path('password_reset/', views.password_reset, name='password-reset'),
    path('password_reset_confirm/<str:uidb64>/<str:token>/', views.password_reset_confirm,
         name='password_reset_confirm'),
    path('password_change/', views.password_change, name='password-change'),
]
