from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import icmp_results, targets

class IcmpResultsSerializer(serializers.ModelSerializer):

    class Meta:
        model = icmp_results
        #fields = "__all__"
        fields = ['created', 'name', 'address', 'success', 'rtt_min', 'rtt_avg', 'rtt_max', 'packetloss', 'transmitted', 'received', 'username']


class TargetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = targets
        #fields = ['name', 'address', 'icmp_size', 'icmp_count', 'icmp_interval']
        fields = "__all__"