#!/usr/bin/env python
from django.db import models
from django.utils import timezone

class targets(models.Model):
    name = models.CharField(primary_key = True, max_length = 255)
    icmp = models.BooleanField(default = False)
    dns = models.BooleanField(default = False)
    created = models.DateTimeField(default = timezone.now)
    modified = models.DateTimeField(default = timezone.now)
    address = models.CharField(null=True, max_length = 255)
    icmp_size = models.IntegerField(null=True, default = 500)
    icmp_interval = models.IntegerField(null=True, default=1)
    icmp_count = models.IntegerField(null=True, default=5)

    class Meta:
        verbose_name_plural = "targets"

    def __str__(self):
        return self.name

class icmp_results(models.Model):
    name = models.CharField(max_length=255, blank=False)
    address = models.CharField(max_length=255, blank=True)
    icmp_size = models.IntegerField(null=True, default = 0)
    icmp_interval = models.IntegerField(null=True, default = 0)
    icmp_count = models.IntegerField(null=True, default = 0)
    created = models.DateTimeField(default = timezone.now)
    #rtt_avg = models.CharField(null=True, max_length = 255)
    rtt_avg = models.FloatField(null=True)
    rtt_max = models.FloatField(null=True)
    rtt_min = models.FloatField(null=True)
    packetloss = models.IntegerField(default=0)
    received = models.IntegerField(default=0)
    transmitted = models.IntegerField(default=0)
    success = models.BooleanField(default=False)
    results = models.CharField(null=True, max_length=1000)
    username = models.CharField(null=True, max_length=255)

    class Meta:
        verbose_name_plural = "icmp_results"

    def __str__(self):
        return self.name

class dns_results(models.Model):
    name = models.CharField(max_length=255, blank=False)
    target = models.CharField(max_length=255, blank=True)
    ttl_time = models.CharField(max_length=255, blank=True)
    protocol = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    last_state = models.CharField(max_length=255, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "dns_results"

    def __str__(self):
        return self.name