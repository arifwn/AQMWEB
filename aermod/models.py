
import json
import urllib

from django.db import models
from django.contrib.auth.models import User
from django.test import TestCase
from django.db.models.signals import pre_save, post_save, pre_delete
from django.core.urlresolvers import reverse


class Setting(models.Model):
    '''setting model'''
    user = models.ForeignKey(User, db_index=True, related_name='aermod_setting')
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    
    hillheight_setting = models.TextField(blank=True)
    meteorology_setting = models.TextField(blank=True)
    aermod_setting = models.TextField(blank=True)
    plot_setting = models.TextField(blank=True)
    is_removed = models.BooleanField(default=False, db_index=True)
    
    def __unicode__(self):
        return str(self.id)
    
    class Meta:
        verbose_name  = 'Setting'
        verbose_name_plural  = 'Settings'
    

class Task(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    user = models.ForeignKey(User, db_index=True, related_name='aermod_task')
    setting = models.ForeignKey(Setting, related_name='task');
    
    stage_list = ['Meteorological Data Extraction', 'Terrain Data Generation',
                  'AERMET', 'AERMOD', 'Processing AERMOD Results']

    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name  = 'Task'
        verbose_name_plural  = 'Tasks'
    
    def get_kind(self):
        '''Return the kind of model this task represent.'''
        return 'aermod'
    
    @property
    def kind(self):
        return self.get_kind()
    
    @models.permalink
    def get_url(self):
        return ('aermod-task-detail', [str(self.id)])
    
    @models.permalink
    def get_rest_url(self):
        return ('rest-aermod-task', [str(self.id)])
    
    def get_status(self):
        ''' Get current task status: draft, running, finished, pending, error '''
        try:
            if self.queue.status == 'finished':
                if self.queue.is_error:
                    return 'error'
            return self.queue.status
        except TaskQueue.DoesNotExist:
            return 'draft'
    
    def get_stage(self):
        ''' Get current task stage. '''
        try:
            return self.queue.stage
        except TaskQueue.DoesNotExist:
            return ''
    
    def get_progress_percent(self):
        ''' Get current task progress completion in percent. '''
        try:
            stage = self.queue.stage
        except TaskQueue.DoesNotExist:
            return 0
        
        if len(stage.strip()) == 0:
            return 0
        
        if self.queue.status == 'pending':
            return 0
        elif (self.queue.status == 'finished') and not self.queue.is_error:
            return 100
        
        try:
            index = self.stage_list.index(stage)
        except ValueError:
            return -1
        
        percent = (float(index) / float(len(self.stage_list))) * 100.0
        return int(percent)


class TaskGroup(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    user = models.ForeignKey(User, db_index=True, related_name='aermod_taskgroup')
    tasks = models.ManyToManyField(Task, related_name='groups', blank=True, null=True)
    
    is_running = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name  = 'TaskGroup'
        verbose_name_plural  = 'TaskGroups'


class TaskQueue(models.Model):
    ''' The queue to be consumed by RPC Server '''
    # Caution: there should not be any duplicated entry for the same task!
    created = models.DateTimeField(auto_now_add=True, editable=False)
    task = models.OneToOneField(Task, related_name='queue')
    
    # Which RPC Server assigned this task
    server = models.ForeignKey('aqm_web.Server', blank=True, null=True, related_name='aermod_taskqueue')
    envid = models.IntegerField(blank=True, null=True)
    
    STATUS_TYPE = [('pending', 'Pending'),
        ('running', 'Running'),
        ('finished', 'Finished'),
        ('canceled', 'Canceled')]
    status = models.CharField(max_length=20, db_index=True,
                              choices=STATUS_TYPE, default='pending')
    
    # Currently running stage
    stage = models.CharField(max_length=200, blank=True, db_index=True)
    
    # If RPC Server failed when processing this entry, the reason can be found
    # here
    is_error = models.BooleanField(default=False)
    error_log = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.task.name
    
    class Meta:
        verbose_name  = 'TaskQueue'
        verbose_name_plural  = 'TaskQueues'

