from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.context_managers import cd, lcd
import datetime

env.hosts = []

def dump_data():
    '''Dump primary data into a database fixtures'''
    
    local('python manage.py dumpdata --indent=4 --exclude=admin.logentry --exclude=contenttypes --exclude=contenttypes --exclude=sessions --exclude=auth.permission > dump.json')

def dump_db():
    dump_prefix = 'backup-drop-if-exist-%s' % datetime.datetime.now().strftime('%Y-%m-%d-T-%H-%M-%S')
    local('mysqldump --user=root aqmweb > dbdump/%s.sql' % dump_prefix)

def compile_less():
    local('lessc --compress aqm_web/static/aqm_web/less/main/main.less > aqm_web/static/aqm_web/css/main.css')
    
def compile_coffee():
    local('coffee -o aqm_web/static/aqm_web/js -c aqm_web/static/aqm_web/coffee/*.coffee')

def get_all_files(directory, ext='.py'):
    import os
    
    ext_index = -len(ext)
    file_list = []
    
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f[ext_index:] == ext:
                file_list.append(os.path.join(root, f))
    
    return file_list

def count_line():
    ''' Count total line number of select files.
        find . -name '*.py' | xargs wc -l
    '''
    
    from cStringIO import StringIO
    
    f = {}
    name = 'aqm_utils'
    f['%s_py' % name] = get_all_files(name, '.py')
    f['%s_html' % name] = get_all_files(name, '.html')
    f['%s_js' % name] = get_all_files(name, '.js')
    f['%s_coffee' % name] = get_all_files(name, '.coffee')
    f['%s_less' % name] = get_all_files(name, '.less')
    
    name = 'aqm_web'
    f['%s_py' % name] = get_all_files(name, '.py')
    f['%s_html' % name] = get_all_files(name, '.html')
    f['%s_js' % name] = get_all_files(name, '.js')
    f['%s_coffee' % name] = get_all_files(name, '.coffee')
    f['%s_less' % name] = get_all_files(name, '.less')
    
    name = 'user_profile'
    f['%s_py' % name] = get_all_files(name, '.py')
    f['%s_html' % name] = get_all_files(name, '.html')
    f['%s_js' % name] = get_all_files(name, '.js')
    f['%s_coffee' % name] = get_all_files(name, '.coffee')
    f['%s_less' % name] = get_all_files(name, '.less')
    
    name = 'wrf'
    f['%s_py' % name] = get_all_files(name, '.py')
    f['%s_html' % name] = get_all_files(name, '.html')
    f['%s_js' % name] = get_all_files(name, '.js')
    f['%s_coffee' % name] = get_all_files(name, '.coffee')
    f['%s_less' % name] = get_all_files(name, '.less')
    
    exclude_list = ['bootstrap', 'jquery', 'codemirror',
                    'canvas-1.2.', 'less-1.1.3']
    
    file_list_nonfiltered = []
    file_list = []
    for key, val in f.iteritems():
        if len(val) > 0:
            file_list_nonfiltered.extend(val)
    
    for f in file_list_nonfiltered:
        skip = False
        for exclude in exclude_list:
            if exclude in f:
                skip = True
        if skip:
            continue
        file_list.append(f)
    
    file_list_buffer = StringIO()
    
    file_list_buffer.write('wc -l ')
    
    for f in file_list:
        file_list_buffer.write(f)
        file_list_buffer.write(' ')
        
    cmd = file_list_buffer.getvalue()
    
    if len(file_list) > 0:
        local(cmd)

def update_deployment():
    '''Update deployment code.'''
    
    deployment_target = '~/AQMSystem/deploy/aqmweb'
    local('rm -rf %s/aermod' % deployment_target)
    local('cp -rf aermod %s/' % deployment_target)
    
    local('rm -rf %s/aqm_utils' % deployment_target)
    local('cp -rf aqm_utils %s/' % deployment_target)
    
    local('rm -rf %s/aqm_web' % deployment_target)
    local('cp -rf aqm_web %s/' % deployment_target)
    
    local('rm -rf %s/debug_toolbar' % deployment_target)
    local('cp -rf debug_toolbar %s/' % deployment_target)
    
    local('rm -rf %s/django_extensions' % deployment_target)
    local('cp -rf django_extensions %s/' % deployment_target)
    
    local('rm -rf %s/filebrowser' % deployment_target)
    local('cp -rf filebrowser %s/' % deployment_target)
    
    local('rm -rf %s/grappelli' % deployment_target)
    local('cp -rf grappelli %s/' % deployment_target)
    
    local('rm -rf %s/openpyxl' % deployment_target)
    local('cp -rf openpyxl %s/' % deployment_target)
    
    local('rm -rf %s/piston' % deployment_target)
    local('cp -rf piston %s/' % deployment_target)
    
    local('rm -rf %s/redis_cache' % deployment_target)
    local('cp -rf redis_cache %s/' % deployment_target)
    
    local('rm -rf %s/tinymce' % deployment_target)
    local('cp -rf tinymce %s/' % deployment_target)
    
    local('rm -rf %s/twisted' % deployment_target)
    local('cp -rf twisted %s/' % deployment_target)
    
    local('rm -rf %s/twisted_wsgi' % deployment_target)
    local('cp -rf twisted_wsgi %s/' % deployment_target)
    
    local('rm -rf %s/user_profile' % deployment_target)
    local('cp -rf user_profile %s/' % deployment_target)
    
    local('rm -rf %s/wrf' % deployment_target)
    local('cp -rf wrf %s/' % deployment_target)
    
    local('cp -rf BeautifulSoup.py %s/' % deployment_target)
    local('cp -rf fabfile.py %s/' % deployment_target)
    local('cp -rf manage.py %s/' % deployment_target)
    
    with lcd(deployment_target):
        local('python2.7 manage.py collectstatic')
    
    