from home import views
from django.urls import path



urlpatterns = [
    path('', views.main, name='main'),
    path('home/', views.home, name='home'),
    path('payment/', views.tomorrow, name='payment'),
    path('stats/', views.tomorrow, name='stats'),
    path('help/', views.tomorrow, name='help'),
    path('profile/', views.profile, name='profile'),
    path('database-mode/', views.db_mode, name='db_mode'),
    path('new-database-mode/', views.new_db_mode, name='new_db_mode'),
    path('default-mode/', views.default_mode, name='default_mode'),
    path('amo-register/', views.amo_register, name='amo_register'),
    path('api/v1/home/get_stages_by_pipeline/', views.get_stages_by_pipeline, name='_get_stages_by_pipeline'),
    path('api/v1/home/set_stage_by_pipeline/', views.set_stage_by_pipeline, name='_set_stage_by_pipeline'),
    path('api/v1/home/update-mode/', views.update_mode, name='update_mode'),
    path('api/v1/home/update-db-file', views.update_db_file, name='update_db_file'),
    path('api/v1/home/update-new-db-file', views.update_new_db_file, name='update_new_db_file'),
    path('api/v1/home/update-token', views.update_token, name='update_token'),
    path('api/v1/home/syncronize-amo', views.syncronize_amo, name='syncronize_amo'),
    path('api/v1/home/update-db-rules/', views.update_db_rules, name='update_db_rules'),
    path('api/v1/home/update-new-db-rules/', views.update_new_db_rules, name='update_new_db_rules')
]