"""
URL configuration for littlelemon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from restaurant.views import UserViewSet
from django.contrib.auth.views import LoginView
# urls.py

from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api',include(router.urls)),
    path('restaurant/', include('restaurant.urls')),
    path('auth/',include('djoser.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/',include('djoser.urls.jwt')),
    path('accounts/', include('django.contrib.auth.urls')),  # Include authentication URLs
    path('accounts/login/', LoginView.as_view(template_name='registration/login.html'), name='login'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)