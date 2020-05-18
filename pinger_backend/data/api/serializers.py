from django.contrib.auth.models import User
from rest_framework import serializers
from collector.models import icmp_results, targets
from .models import UserTargets

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']

class UserTargetSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        self.fields['user'] =  UserSerializer(read_only=True)
        return super(UserTargetSerializer, self).to_representation(instance)

    class Meta:
        model = UserTargets
        fields = ['id', 'user_id', 'target_name', 'target_address', 'icmp_size', 'icmp_interval', 'icmp_count', 'user']

