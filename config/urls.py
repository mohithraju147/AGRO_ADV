from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Customize admin site branding
admin.site.site_header = "🌾 Agro-Adv Admin"
admin.site.site_title = "Agro-Adv Portal"
admin.site.index_title = "Welcome to Agro-Adv Dashboard"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.farmers.urls')),
    path('api/', include('apps.crops.api_urls')),
    path('api/', include('apps.market.urls')),
    path('api/', include('apps.predictions.api_urls')),
    path('api/', include('apps.schemes.urls')),
    path('', include('apps.predictions.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
