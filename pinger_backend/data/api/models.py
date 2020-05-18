from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

# Create your models here.

class UserTargets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target_name = models.CharField(max_length=100)
    target_address = models.CharField(null=True, max_length = 255)
    icmp_size = models.IntegerField(null=True, default = 500, validators=[MinValueValidator(100), MaxValueValidator(1000)])
    icmp_interval = models.IntegerField(null=True, default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    icmp_count = models.IntegerField(null=True, default=5, validators=[MinValueValidator(5), MaxValueValidator(10)]) 

    class Meta:
        verbose_name = "User Target"
        verbose_name_plural = "User Targets"
        unique_together = (('user', 'target_name'),)
        unique_together = (('user', 'target_address'),)
        index_together = (('user', 'target_name'),)
        index_together = (('user', 'target_address'),)

    def __str__(self):
        return str(self.user) + " - " + self.target_name + " - " + self.target_address