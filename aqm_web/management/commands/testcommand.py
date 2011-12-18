from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from optparse import make_option
import os
import sys

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--noreload', action='store_false', dest='use_reloader', default=True,
            help='Tells Django to NOT use the auto-reloader.'),
        make_option('--adminmedia', dest='admin_media_path', default='',
            help='Specifies the directory from which to serve admin media.'),
    )
    help = "Starts a lightweight concurrent development web server."
    args = '[optional port number, or ipaddr:port]'

    if hasattr(settings, 'RUNSERVER_DEFAULT_ADDR'):
        DEFAULT_ADDR = settings.RUNSERVER_DEFAULT_ADDR
    else:
        DEFAULT_ADDR = '127.0.0.1'
    if hasattr(settings, 'RUNSERVER_DEFAULT_PORT'):
        DEFAULT_PORT = str(settings.RUNSERVER_DEFAULT_PORT)
    else:
        DEFAULT_PORT = '8000'

    # Validation is called explicitly each time the server is reloaded.
    requires_model_validation = False

    def handle(self, addrport='', *args, **options):
        print 'test command'
