from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions, generics
from .serializers import UserSerializer, ProfileSerializer, UserTargetSerializer
from collector.serializers import IcmpResultsSerializer, TargetsSerializer
from collector.models import icmp_results, targets
from .models import UserTargets
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    #permission_classes = [permissions.IsAdminUser]

class IcmpResultsViewSet(viewsets.ModelViewSet):
    queryset = icmp_results.objects.all().order_by('-id')
    serializer_class = IcmpResultsSerializer
    permission_classes = [permissions.IsAuthenticated]

class TargetsViewSet(viewsets.ModelViewSet):
    queryset = targets.objects.all()
    serializer_class = TargetsSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserIdViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.action == 'list':
            return User.objects.filter(id=self.request.user.id)
        return self.queryset

    #def get_queryset(self):
    #    return User.objects.filter(id=self.request.user.id)

class UserTargetsViewSet(viewsets.ModelViewSet):
    queryset = UserTargets.objects.all()
    serializer_class = UserTargetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.action == 'list':
            return self.queryset.filter(user=self.request.user)
        return self.queryset