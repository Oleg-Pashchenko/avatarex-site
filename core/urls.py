from django.urls import path, include

urlpatterns = [
    path("admin/", include('admin.urls')),
    path('auth/', include('auth_block.urls')),
    path('', include('home.urls'))
]


from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)