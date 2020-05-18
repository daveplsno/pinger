from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from .views import UserViewSet, IcmpResultsViewSet, TargetsViewSet, UserIdViewSet, UserTargetsViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('icmp_results', IcmpResultsViewSet)
router.register('targets', TargetsViewSet)
router.register('user-id', UserIdViewSet, '')

router2 = routers.DefaultRouter()
router2.register('users', UserViewSet)
router2.register('user-targets', UserTargetsViewSet, '')
router2.register('icmp_results', IcmpResultsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('v2/', include(router2.urls)),

]