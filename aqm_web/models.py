from django.db import models
from django.contrib.auth.models import User
from django.test import TestCase


# ------------ Server Models -------------

class ServerTask(models.Model):
    from wrf.models import Task as WRFTask
    task_capacity = models.IntegerField()
    current_queue = models.ManyToManyField(WRFTask, related_name='server', blank=True, null=True)


class ServerInfo(models.Model):
    max_cpu = models.IntegerField(default=100, help_text="in percent")
    max_memory = models.IntegerField(default=8192, help_text="in megabyte")
    max_storage = models.IntegerField(default=1048576, help_text="in megabyte")


class ServerStatus(models.Model):
    cpu = models.IntegerField(default=100, help_text="in percent")
    memory = models.IntegerField(default=8192, help_text="in megabyte")
    storage = models.IntegerField(default=1048576, help_text="in megabyte")
    uptime = models.TimeField()
    updated = models.DateTimeField(auto_now=True, editable=False)


class Server(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    address = models.CharField(max_length=100)
    port = models.IntegerField()
    server_task = models.ForeignKey(ServerTask)
    server_info = models.ForeignKey(ServerInfo)
    server_status = models.ForeignKey(ServerStatus)

    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name  = 'Server'
        verbose_name_plural  = 'Server'
        