from auth_block import views
from django.urls import path

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('amo/', views.amo, name="amo")
]
