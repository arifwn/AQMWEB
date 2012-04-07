
from django.db import models
from django.contrib.auth.models import User
from django.test import TestCase
from django.db.models.signals import pre_save, post_save, pre_delete
import json
from wrf import __version__ as wrf_version
from aqm_utils.datafile import get_excel_worksheets


class Setting(models.Model):
    '''setting model'''
    name = models.CharField(max_length=200, db_index=True)
    user = models.ForeignKey(User, db_index=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    namelist_wrf = models.TextField(blank=True)
    namelist_wps = models.TextField(blank=True)
    namelist_arwpost = models.TextField(blank=True)
    chemdata = models.ForeignKey('ChemData', blank=True, null=True)
    is_removed = models.BooleanField(default=False, db_index=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name  = 'Setting'
        verbose_name_plural  = 'Settings'
    
    def get_max_dom(self):
        ''' Get the number of domain from WPS namelist '''
        from wrf.namelist.decode import decode_namelist_string
        
        namelist_wps = getattr(self, 'parsed_namelist_wps', None)
        if namelist_wps is None:
            namelist_wps = decode_namelist_string(self.namelist_wps)
        
        try:
            res = namelist_wps['share']['max_dom'][0]
        except:
            res = None
        
        return res
    
    def get_start_date(self):
        ''' Return start date from WPS namelist as datetime object '''
        from wrf.namelist.decode import decode_namelist_string
        from wrf.namelist.misc import parse_date_string
        
        namelist_wps = getattr(self, 'parsed_namelist_wps', None)
        if namelist_wps is None:
            namelist_wps = decode_namelist_string(self.namelist_wps)
        
        try:
            res = parse_date_string(namelist_wps['share']['start_date'][0])
        except:
            res = None
        
        return res
    
    def get_end_date(self):
        ''' Return start date from WPS namelist as datetime object '''
        from wrf.namelist.decode import decode_namelist_string
        from wrf.namelist.misc import parse_date_string
        
        namelist_wps = getattr(self, 'parsed_namelist_wps', None)
        if namelist_wps is None:
            namelist_wps = decode_namelist_string(self.namelist_wps)
        
        try:
            res = parse_date_string(namelist_wps['share']['end_date'][0])
        except:
            res = None
        
        return res
    
    
class BaseSetting(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    user = models.ForeignKey(User, db_index=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    namelist_wrf = models.TextField()
    namelist_wps = models.TextField()
    namelist_arwpost = models.TextField(blank=True)
    is_removed = models.BooleanField(default=False, db_index=True)
    
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
    is_removed = models.BooleanField(default=False, db_index=True)
    
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
    is_removed = models.BooleanField(default=False, db_index=True)
    
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
    setting = models.ForeignKey(Setting);

    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name  = 'Task'
        verbose_name_plural  = 'Tasks'
    
    def get_status(self):
        ''' Get current task status: draft, running, finished, pending, error '''
        if self.finished_entry.count() > 0:
            if self.finished_entry.is_error:
                return 'error'
            else:
                return 'finished'
        elif self.running_entry.count() > 0:
            return 'running'
        elif self.queue_entry.count() > 0:
            return 'pending'
        else:
            return 'draft'


class TaskGroup(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    user = models.ForeignKey(User, db_index=True)
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
    task = models.ForeignKey(Task, related_name='queue_entry')
    
    class Meta:
        verbose_name  = 'TaskQueue'
        verbose_name_plural  = 'TaskQueues'


class RunningTask(models.Model):
    # When consuming task, an entry put in this table to represent running task
    # and the source item in TaskQueue is deleted
    # Caution: there should not be any duplicated entry for the same task!
    created = models.DateTimeField(auto_now_add=True, editable=False)
    task = models.ForeignKey(Task, related_name='running_entry')
    
    # Which RPC Server consumed this task
    server = models.ForeignKey('aqm_web.Server')
    envid = models.IntegerField()
    
    # Currently running stage
    stage = models.CharField(max_length=200, blank=True, db_index=True)
    
    class Meta:
        verbose_name  = 'RunningTask'
        verbose_name_plural  = 'RunningTasks'


class FinishedTask(models.Model):
    # When finished with the task, an entry put in this table
    # and the source item in RunningTask is deleted
    # Caution: there should not be any duplicated entry for the same task!
    created = models.DateTimeField(auto_now_add=True, editable=False)
    task = models.ForeignKey(Task, related_name='finished_entry')
    
    # Which RPC Server consumed this task
    server = models.ForeignKey('aqm_web.Server')
    envid = models.IntegerField()
    
    # Last running stage
    stage = models.CharField(max_length=200, blank=True, db_index=True)
    
    # If RPC Server failed when processing this entry, the reason can be found
    # here
    is_error = models.BooleanField(default=False)
    error_log = models.TextField(blank=True)
    
    class Meta:
        verbose_name  = 'FinishedTask'
        verbose_name_plural  = 'FinishedTasks'
        

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

#def presave_process_excel_chemdata(sender, instance, **kwargs):
#    ''''''
#    instance.data.flush()
#    path = instance.data.path
#    worksheets = get_excel_worksheets(path)
#    if worksheets is not None:
#        json_dmp = json.dumps(worksheets)
#        instance.worksheets = json_dmp
#        instance.save()
#            
#pre_save.connect(presave_process_excel_chemdata, sender=ChemData)

def predelete_chemdata(sender, instance, **kwargs):
    '''Delete uploaded data'''
    try:
        instance.data.delete()
    except:
        pass
    
            
pre_delete.connect(predelete_chemdata, sender=ChemData)
