"""pinger URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib.auth.models import User, Group
from rest_framework import routers, serializers, viewsets
from rest_framework.authtoken import views as whatever
from collector import views
from api import views
from django.views.static import serve 


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'icmp_results', views.IcmpResultsViewSet)
router.register(r'targets', views.TargetsViewSet)
router.register(r'user-id', views.UserIdViewSet, 'idk')



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #path('api-token-auth/', whatever.obtain_auth_token, name='api-tokn-auth'),
    #path('api-token-auth/', whatever.obtain_auth_token),
]