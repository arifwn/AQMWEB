from django.db import models
from django.contrib.auth.models import User
from django.test import TestCase


# ------------ Server Models -------------

class Server(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    address = models.CharField(max_length=100)
    port = models.IntegerField()    
    max_cpu = models.IntegerField(default=100, help_text="in percent")
    max_memory = models.IntegerField(default=8192, help_text="in megabyte")
    max_storage = models.IntegerField(default=1048576, help_text="in megabyte")

    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name  = 'Server'
        verbose_name_plural  = 'Server'
        