#!/usr/bin/env python
from django.db import models
from django.utils import timezone

class targets(models.Model):
    name = models.CharField(primary_key=True, max_length=255, blank=False)
    icmp = models.BooleanField(default=False)
    dns = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)
    target = models.CharField(max_length=255, blank=False, null=True)
    icmp_size = models.CharField(max_length=255, blank=False, null=True,default=500)
    icmp_interval = models.CharField(max_length=255, blank=False, null=True, default=1)
    icmp_count = models.CharField(max_length=255, blank=False, null=True, default=10)

    class Meta:
        verbose_name_plural = "targets"

    def __str__(self):
        return self.name

class icmp_results(models.Model):
    name = models.CharField(max_length=255, blank=False)
    target = models.CharField(max_length=255, blank=True)
    size = models.CharField(max_length=255, blank=True)
    count = models.CharField(max_length=255, blank=True)
    created = models.DateTimeField(default=timezone.now)
    min_rtt = models.CharField(max_length=255, default=0)
    max_rtt = models.CharField(max_length=255, default=0)
    avg_rtt = models.CharField(max_length=255, default=0)
    success = models.BooleanField(default=False)
    packet_success = models.CharField(max_length=255, default=0)
    packet_fail = models.CharField(max_length=255, default=0)
    loss_percentage = models.CharField(max_length=255, default=0)

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