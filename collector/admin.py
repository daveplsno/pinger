from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(targets)
admin.site.register(icmp_results)
admin.site.register(dns_results)