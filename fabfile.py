from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.context_managers import cd, lcd

env.hosts = []

def dump_data():
    '''Dump primary data into a database fixtures'''
    
    local('python manage.py dumpdata --indent=4 --exclude=contenttypes --exclude=contenttypes --exclude=sessions --exclude=auth.permission > aqm_web/fixtures/initial_data.json')

