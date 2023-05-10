"""backend URL Configuration

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
from django.contrib import admin
from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularRedocView, SpectacularSwaggerView, RedirectView, SpectacularJSONAPIView
from django.views.static import serve
from backend.settings import MEDIA_ROOT
urlpatterns = [
    path('', RedirectView.as_view(url='docs')),
    path('swagger/json/', SpectacularJSONAPIView.as_view(), name='schema'),
    # Optional UI:
    path('swagger/ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('swagger/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # My patterns:
    path('admin/', admin.site.urls),
    path("api/", include("LunchTime.urls")),
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root":MEDIA_ROOT}), 
]
