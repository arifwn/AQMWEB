from django.db import models
from django.contrib.auth.models import User
from django.test import TestCase


# ------------ Server Models -------------

class Server(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    address = models.CharField(max_length=100)
    port = models.IntegerField()
    user = models.ForeignKey(User, db_index=True)
    is_enabled = models.BooleanField(default=True, db_index=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name  = 'Server'
        verbose_name_plural  = 'Server'
    
    @models.permalink
    def get_rest_url(self):
        return ('rest-server-detail', [str(self.id)])
    
    @models.permalink
    def get_status_rest_url(self):
        return ('rest-server-utilization', [str(self.id)])
    