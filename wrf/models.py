
from django.db import models
from django.contrib.auth.models import User
from django.test import TestCase
import json
from wrf import __version__ as wrf_version
from namelist import encode as n_enc
from namelist import decode as n_dec


class Domain(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    user = models.ForeignKey(User, db_index=True)
    
    width = models.IntegerField()
    height = models.IntegerField()
    dx = models.FloatField(blank=True, null=True)
    dy = models.FloatField(blank=True, null=True)
    
    parent = models.ForeignKey('self', related_name='childs', blank=True, 
                               null=True)
    ratio = models.IntegerField(blank=True, null=True)
    i_parent_start = models.IntegerField(blank=True, null=True)
    j_parent_start = models.IntegerField(blank=True, null=True)
    
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name  = 'Domain'
        verbose_name_plural  = 'Domain'


class Setting(models.Model):
    '''setting model'''
    name = models.CharField(max_length=200, db_index=True)
    user = models.ForeignKey(User, db_index=True)
    description = models.TextField()
    setting_json = models.TextField(blank=True, null=True)
    setting_version = models.TextField(blank=True, null=True)
    generated_namelist = models.TextField(blank=True, null=True)
    user_namelist_wrf = models.TextField(blank=True, null=True)
    user_namelist_wps = models.TextField(blank=True, null=True)
    
    removed = models.BooleanField(default=False, db_index=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name  = 'Setting'
        verbose_name_plural  = 'Setting'
    
    def clean(self):
        if self.setting_version is None:
            self.setting_version = wrf_version
        if self.setting_json is not None:
            parsed_data = json.loads(self.setting_json)
            self.generated_namelist = n_enc.encode_namelist(parsed_data)
    
    def load_namelist(self, namelist_data):
        data = n_dec.decode_namelist_string(namelist_data)
        json_data = json.dumps(data)
        self.setting_json = json_data
    
    def get_setting(self):
        data = json.loads(self.setting_json)
        

class ChemData(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    user = models.ForeignKey(User, db_index=True)
    data = models.FileField(upload_to='wrf/chem_data/%Y/%m/', max_length=200)
    DATA_TYPE_CHOICE = (
        ('xlsx', 'Excel 2007 (*.xlsx)'),
        ('csv', 'Comma-Separated Value (*.csv)'),
    )
    data_type = models.CharField(max_length=10, choices=DATA_TYPE_CHOICE, 
                                 db_index=True)
    removed = models.BooleanField(default=False, db_index=True)
    
    class Meta:
        verbose_name  = 'ChemData'
        verbose_name_plural  = 'ChemData'
    
    def __unicode__(self):
        return self.name
        

class AltMeteoData(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    user = models.ForeignKey(User, db_index=True)
    data = models.FileField(upload_to='wrf/alt_meteo_data/%Y/%m/', max_length=200)
    DATA_TYPE_CHOICE = (
        ('netcdf', 'NetCDF'),
        ('grib2', 'GRIB2'),
        ('grib1', 'GRIB1'),
    )
    data_type = models.CharField(max_length=10, choices=DATA_TYPE_CHOICE, 
                                 db_index=True)
    removed = models.BooleanField(default=False, db_index=True)
    
    class Meta:
        verbose_name  = 'AltMeteoData'
        verbose_name_plural  = 'AltMeteoData'
    
    def __unicode__(self):
        return self.name
        

class Task(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    user = models.ForeignKey(User, db_index=True)
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    
    # coordinate settings
    PROJECTION_TYPE_CHOICE = (
        ('mercator', 'Mercator'),
        ('lambert', 'Lambert Conformal'),
        ('polar', 'Polar Stereographic'),
        ('cylindrical', 'Regular Latitude-Longitude / Cylindrical Equidistant'),
    )
    projection = models.CharField(max_length=20, choices=PROJECTION_TYPE_CHOICE)
    true_lat_1 = models.FloatField(blank=True, null=True)
    true_lat_2 = models.FloatField(blank=True, null=True)
    stand_lon = models.FloatField(blank=True, null=True)
    pole_lat = models.FloatField(blank=True, null=True)
    pole_lon = models.FloatField(blank=True, null=True)
    
    domains = models.ManyToManyField(Domain)
    setting = models.ForeignKey(Setting);

    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name  = 'Task'
        verbose_name_plural  = 'Task'


class TaskGroup(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    user = models.ForeignKey(User, db_index=True)
    tasks = models.ManyToManyField(Task, related_name="groups")
    
    running = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name  = 'TaskGroup'
        verbose_name_plural  = 'TaskGroup'


class TaskQueue(models.Model):
    submitted_date = models.DateTimeField(auto_now_add=True, db_index=True)
    processed_date = models.DateTimeField(blank=True, null=True)
    finished_date = models.DateTimeField(blank=True, null=True)
    is_running = models.BooleanField(default=False, db_index=True)
    is_finished = models.BooleanField(default=False, db_index=True)
    task = models.ForeignKey(Task, related_name='queues')
    
    class Meta:
        verbose_name  = 'TaskQueue'
        verbose_name_plural  = 'TaskQueue'
        
    # if the task is not finished and not running, task consumer can process 
    # this task and set is_running to True. When finished, set is_running to
    # false and is_finished to True

