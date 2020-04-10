from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import icmp_results, targets

class IcmpResultsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = icmp_results
        fields = ('name', 'target', 'size', 'count', 'created', 'min_rtt', 'max_rtt', 'avg_rtt', 'success', 'packet_success', 'packet_fail', 'loss_percentage')

class TargetsSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = targets
        fields = ('name', 'icmp', 'dns', 'target', 'icmp_size', 'icmp_count')