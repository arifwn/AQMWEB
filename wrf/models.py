
import json
import urllib

from django.db import models
from django.contrib.auth.models import User
from django.test import TestCase
from django.db.models.signals import pre_save, post_save, pre_delete
from django.core.urlresolvers import reverse

from aqm_utils.datafile import get_excel_worksheets

from wrf import __version__ as wrf_version
from wrf.namelist.decode import decode_namelist_string
from wrf.namelist.misc import parse_date_string


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
    grads_template = models.TextField(blank=True)
    chemdata = models.ForeignKey('ChemData', blank=True, null=True)
    is_removed = models.BooleanField(default=False, db_index=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name  = 'Setting'
        verbose_name_plural  = 'Settings'
    
    def get_wps_namelist_data(self, section, param, domain):
        '''
        Return namelist data.
        Raise KeyError if section or param is invalid.
        Raise IndexError if domain is invalid.
        '''
        namelist_wps = getattr(self, 'parsed_namelist_wps', None)
        if namelist_wps is None:
            namelist_wps = decode_namelist_string(self.namelist_wps)
            self.parsed_namelist_wps = namelist_wps
        
        return namelist_wps[section][param][domain]
    
    def get_max_dom(self):
        ''' Get the number of domain from WPS namelist '''
        return self.get_wps_namelist_data('share', 'max_dom', 0)
    
    @property
    def max_dom(self):
        ''' Alias for get_max_dom() '''
        return self.get_max_dom()
    
    def get_dx(self, domain=0):
        ''' Get dx of domain from WPS namelist '''
        return self.get_wps_namelist_data('geogrid', 'dx', domain)
        
    def get_dy(self, domain=0):
        ''' Get dy of domain from WPS namelist '''
        return self.get_wps_namelist_data('geogrid', 'dy', domain)
    
    @property
    def dx(self):
        ''' Alias for get_dx(domain=0) '''
        return self.get_dx(domain=0)
    
    @property
    def dy(self):
        ''' Alias for get_dy(domain=0) '''
        return self.get_dy(domain=0)
    
    def get_start_date(self, domain=0):
        ''' Return start date from WPS namelist as datetime object '''
        return parse_date_string(self.get_wps_namelist_data('share',
                                                            'start_date',
                                                            domain))
    
    def get_end_date(self, domain=0):
        ''' Return start date from WPS namelist as datetime object '''
        return parse_date_string(self.get_wps_namelist_data('share',
                                                            'end_date',
                                                            domain))
    
    @property
    def start_date(self):
        ''' Alias for get_start_date(domain=0) '''
        return self.get_start_date(domain=0)
    
    @property
    def end_date(self):
        ''' Alias for get_end_date(domain=0) '''
        return self.get_end_date(domain=0)
    
    def get_lat(self, domain=0):
        ''' Get lat of domain from WPS namelist '''
        return self.get_wps_namelist_data('geogrid', 'ref_lat', domain)
    
    def get_lon(self, domain=0):
        ''' Get lon of domain from WPS namelist '''
        return self.get_wps_namelist_data('geogrid', 'ref_lon', domain)
    
    @property
    def lat(self):
        ''' Alias for get_lat(domain=0) '''
        return self.get_lat(domain=0)
    
    @property
    def lon(self):
        ''' Alias for get_lon(domain=0) '''
        return self.get_lon(domain=0)
    
    def get_preview_map(self, projection='mercator'):
        ''' Return a 800x600 preview map url '''
        map_url = reverse('map-preview-mercator')
        data = {}
        data['ref_lat'] = self.get_wps_namelist_data('geogrid', 'ref_lat', 0)
        data['ref_lon'] = self.get_wps_namelist_data('geogrid', 'ref_lon', 0)
        data['upper_lat'] = data['ref_lat'] + 20
        data['upper_lon'] = data['ref_lon'] + 27
        data['lower_lat'] = data['ref_lat'] - 20
        data['lower_lon'] = data['ref_lon'] - 27
        data['true_lat'] = self.get_wps_namelist_data('geogrid', 'truelat1', 0)
        return '%s?%s' % (map_url, urllib.urlencode(data))
        
    @property
    def preview_map(self):
        ''' Alias for get_preview_map() '''
        return self.get_preview_map()
    
    
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
    
    stage_list = ['Model Preparation', 'WPS', 'WRF/Real', 'WRF/Emission',
                  'WRF', 'ARWpost']

    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name  = 'Task'
        verbose_name_plural  = 'Tasks'
    
    
    @models.permalink
    def get_url(self):
        return ('wrf-task-detail', [str(self.id)])
    
    @models.permalink
    def get_rest_url(self):
        return ('rest-task', [str(self.id)])
    
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
    task = models.OneToOneField(Task, related_name='queue')
    
    # Which RPC Server assigned this task
    server = models.ForeignKey('aqm_web.Server',blank=True, null=True)
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
