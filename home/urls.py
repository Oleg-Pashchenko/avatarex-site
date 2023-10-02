from home import views
from django.urls import path



urlpatterns = [
    path('', views.main, name='main'),
    path('home/', views.home, name='home'),
    path('payment/', views.tomorrow, name='payment'),
    path('stats/', views.tomorrow, name='stats'),
    path('help/', views.tomorrow, name='help'),
    path('profile/', views.profile, name='profile'),
    path('db-mode/', views.db_mode, name='db_mode'),
    path('default-mode/', views.default_mode, name='default_mode'),
    path('amo-register/', views.amo_register, name='amo_register'),
    path('api/v1/home/get_stages_by_pipeline/', views.get_stages_by_pipeline, name='_get_stages_by_pipeline')
]