from home import views, api, new_views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.main, name='main'),
    path('home/', views.home, name='home'),
    path('faq/',new_views.faq, name='faq'),
    path('payment/', new_views.payment, name='payment'),
    path('about/', new_views.about, name='about'),
    path('help/', views.tomorrow, name='help'),
    path('profile/', views.profile, name='profile'),
    path('old-database-mode/', views.db_mode, name='db_mode'),
    path('new-database-mode/', views.new_db_mode, name='new_db_mode'),
    path('default-mode/', views.default_mode, name='default_mode'),
    path('amo-register/', views.amo_register, name='amo_register'),
    path('api/v1/home/get_stages_by_pipeline/', views.get_stages_by_pipeline, name='_get_stages_by_pipeline'),
    path('api/v1/home/set_stage_by_pipeline/', views.set_stage_by_pipeline, name='_set_stage_by_pipeline'),
    path('api/v1/home/update-mode/', views.update_mode, name='update_mode'),
    path('api/v1/home/update-db-file', views.update_db_file, name='update_db_file'),
    path('api/v1/home/update-new-db-file', views.update_new_db_file, name='update_new_db_file'),
    path('api/v1/home/update-token', api.update_token, name='update_token'),  # NEW
    path('api/v1/home/syncronize-amo', views.syncronize_amo, name='syncronize_amo'),
    path('api/v1/home/update-db-rules/', views.update_db_rules, name='update_db_rules'),
    path('api/v1/home/update-new-db-rules/', views.update_new_db_rules, name='update_new_db_rules'),
    path('api/v1/home/update-voice/', views.update_voice, name='update_voice'),
    # New handlers
    # VIEWS
    path('prompt-mode/', new_views.prompt_mode, name='prompt_mode_v1'),
    path('database-mode/', new_views.database_mode, name='database_mode_v1'),
    path('knowledge-mode/', new_views.knowledge_mode, name='knowledge_mode_v1'),
    path('database-and-knowledge-mode/', new_views.database_and_knowledge_mode, name='database_and_knowledge_mode'),

    # API
    path('api/v1/update-mode/', api.update_mode, name='update_mode'),
    path('api/v1/update-mode-file-link/', api.update_mode_file_link, name='update_mode_file_link'),

    # Widget
    path('widget', api.widget, name='widget')
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
