from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions, generics
from .serializers import UserSerializer, GroupSerializer, ProfileSerializer
from collector.serializers import IcmpResultsSerializer, TargetsSerializer
from collector.models import icmp_results, targets
# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]

class IcmpResultsViewSet(viewsets.ModelViewSet):
    queryset = icmp_results.objects.all().order_by('-id')
    serializer_class = IcmpResultsSerializer
    permission_classes = [permissions.IsAuthenticated]

class TargetsViewSet(viewsets.ModelViewSet):
    queryset = targets.objects.all()
    serializer_class = TargetsSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserIdViewSet(viewsets.ModelViewSet):
    #queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
