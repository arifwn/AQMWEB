
from django.db import models
from django.contrib.auth.models import User
from django.test import TestCase
from django.db.models.signals import pre_save, post_save
import json
from wrf import __version__ as wrf_version
from namelist import encode as n_enc
from namelist import decode as n_dec
from aqm_utils.datafile import get_excel_worksheets


class Domain(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    user = models.ForeignKey(User, db_index=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
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
        verbose_name_plural  = 'Domains'


class Setting(models.Model):
    '''setting model'''
    name = models.CharField(max_length=200, db_index=True)
    user = models.ForeignKey(User, db_index=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    setting_json = models.TextField(blank=True)
    setting_version = models.TextField(blank=True)
    generated_namelist = models.TextField(blank=True)
    user_namelist_wrf = models.TextField(blank=True)
    user_namelist_wps = models.TextField(blank=True)
    
    base_setting = models.ForeignKey('BaseSetting');
    removed = models.BooleanField(default=False, db_index=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name  = 'Setting'
        verbose_name_plural  = 'Settings'
    
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
    
class BaseSetting(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    user = models.ForeignKey(User, db_index=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    namelist_wrf = models.TextField()
    namelist_wps = models.TextField()
    removed = models.BooleanField(default=False, db_index=True)
    default = models.BooleanField(default=False, db_index=True)
    
    class Meta:
        verbose_name  = 'BaseSetting'
        verbose_name_plural  = 'BaseSettings'
        
    def __unicode__(self):
        return self.name

class PollutantParam(models.Model):
    PLT_TYPE = [('E_ALD', 'ALT'), ('E_CO', 'CO'), 
                ('E_CSL', 'CSL'), ('E_ECI', 'ECI'), 
                ('E_ECJ', 'ECJ)'), ('E_ETH', 'ETH'), 
                ('E_HC3', 'HC3'), ('E_HC5', 'HC5'), 
                ('E_HC8', 'HC8'), ('E_HCHO', 'HCO'), 
                ('E_ISO', 'ISO'), ('E_KET', 'KET'), 
                ('E_NH3', 'NH3'), ('E_NO', 'NO'), 
                ('E_NO3I', 'NO3I'), ('E_NO3J', 'NO3J'), 
                ('E_OL2', 'OL2'), ('E_OLI', 'OLI'), 
                ('E_OLT', 'OLT'), ('E_ORA2', 'ORA2'), 
                ('E_ORGI', 'ORGI'), ('E_ORGJ', 'ORGJ'), 
                ('E_PM25I', 'PM25I'), ('E_PM25J', 'PM25J'), 
                ('E_PM_10', 'PM_10'), ('E_SO2', 'SO2'), 
                ('E_SO4I', 'SO4I'), ('E_SO4J', 'SO4J'), 
                ('E_TOL', 'TOL'), ('E_XYL', 'XYL')]
    
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    pollutant = models.CharField(max_length=20, choices=PLT_TYPE)
    x = models.CharField(max_length=50)
    y = models.CharField(max_length=50)
    lat = models.CharField(max_length=50)
    lon = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
    conversion_factor = models.FloatField(default=1.0)
    worksheet = models.IntegerField(default=0)
    
    class Meta:
        verbose_name  = 'PollutantParam'
        verbose_name_plural  = 'PollutantParams'
    
    def __unicode__(self):
        return self.pollutant
       
    
class ChemData(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    user = models.ForeignKey(User, db_index=True)
    data = models.FileField(upload_to='wrf/chem_data/%Y/%m/', max_length=200)
    worksheets = models.TextField(blank=True)
    parameters = models.ManyToManyField(PollutantParam, blank=True, null=True)
    removed = models.BooleanField(default=False, db_index=True)
    
    class Meta:
        verbose_name  = 'ChemData'
        verbose_name_plural  = 'ChemData'
    
    def __unicode__(self):
        return self.name
       

class AltMeteoData(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
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
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
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
        verbose_name_plural  = 'Tasks'


class TaskGroup(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    user = models.ForeignKey(User, db_index=True)
    tasks = models.ManyToManyField(Task, related_name="groups")
    
    running = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name  = 'TaskGroup'
        verbose_name_plural  = 'TaskGroups'


class TaskQueue(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    processed = models.DateTimeField(blank=True, null=True)
    finished = models.DateTimeField(blank=True, null=True)
    is_running = models.BooleanField(default=False, db_index=True)
    is_finished = models.BooleanField(default=False, db_index=True)
    task = models.ForeignKey(Task, related_name='queues')
    
    class Meta:
        verbose_name  = 'TaskQueue'
        verbose_name_plural  = 'TaskQueues'
        
    # if the task is not finished and not running, task consumer can process 
    # this task and set is_running to True. When finished, set is_running to
    # false and is_finished to True


# Prepopulate ChemData's worksheet textfield with dict of worksheets
# contained within the selected file

def postsave_process_excel_chemdata(sender, instance, created, **kwargs):
    '''HACK: currently newly uploaded excel file is processed twice,
    perhaps we can use cache to prevent double processing?'''
    path = instance.data.path
    worksheets = get_excel_worksheets(path)
    if worksheets is not None:
        json_dmp = json.dumps(worksheets)
        if json_dmp != instance.worksheets:
            instance.worksheets = json_dmp
            instance.save()
            
post_save.connect(postsave_process_excel_chemdata, sender=ChemData)
