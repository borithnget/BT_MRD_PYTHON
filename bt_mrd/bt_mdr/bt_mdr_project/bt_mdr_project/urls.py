"""bt_mdr_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import django
from django import urls
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView # new
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.conf.urls.static import static

# urlpatterns = [
#     # path('mdr/', include('mdrapp.urls')),
#     path('admin/', admin.site.urls),
#     path("accounts/", include("django.contrib.auth.urls")),
#     path('', TemplateView.as_view(template_name='home.html'), name='home'), # new
#     path('api/', include('myapi.urls')),
#     path('rosetta/', include('rosetta.urls')),  # NEW
# ]

urlpatterns = [
    path(r'^i18n/', include(django.conf.urls.i18n)),
]


urlpatterns += i18n_patterns (
    # path('mdr/', include('mdrapp.urls')),
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    # path('', TemplateView.as_view(template_name='home.html'), name='home'), # new
    path('api/', include('myapi.urls'), name="api"),
    path('rosetta/', include('rosetta.urls')),  # NEW
    path('watersupply/', include('watersupply.urls')),
    path('report/', include('report.urls')),
    path('ajax/', include('ajax.urls')),
    path('app/', include('mdrapp.urls')),
    path(r'', include('mdrapp.urls'))
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)