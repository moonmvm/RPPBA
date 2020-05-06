from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "RPPBA ADMIN"
admin.site.site_title = "RPPBA ADMIN"
admin.site.index_title = "RPPBA Administration panel"

API_PATTERNS = [
    path('', include('warehouse.urls')),
    path('', include('waybills.urls')),
    path('', include('products.urls')),
    path('', include('users.urls')),
]

urlpatterns = [
    path('', admin.site.urls),
    path('api/', include(API_PATTERNS)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
