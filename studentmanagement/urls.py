from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('', include('education.urls')),
    path('accounts/', include('accounts.urls')),
    path('education/', include('education.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



