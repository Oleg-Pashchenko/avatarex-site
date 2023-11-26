from admin import views
from django.urls import path

urlpatterns = [
    path('', views.enter_secret_code_page, name='enter_secret_code_page'),

    path('users/', views.users, name='users'),
    path('users/<int:user_id>/', views.user, name='user_detail'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('translations/', views.translations, name='translations')
]
