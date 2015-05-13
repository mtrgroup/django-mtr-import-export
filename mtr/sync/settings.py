import os

import django

from django.conf import settings

# custom prefix for avoiding name colissions
PREFIX = getattr(settings, 'MTR_SYNC_SETTINGS_PREFIX', 'MTR_SYNC')


def getattr_with_prefix(name, default):
    """Shortcut for getting settings attribute with prefix"""

    return lambda: getattr(settings, '{}_{}'.format(PREFIX, name), default)


def strip_media_root(path):
    return path.split(settings.MEDIA_ROOT)[1].lstrip('/')


def get_buffer_file_path(instance, filename, absolute=False):
    """Generate file path for report"""

    action = 'export' if instance.action else 'import'
    path = os.path.join(
        settings.MEDIA_ROOT, 'sync', action, filename.lower())

    if not absolute:
        path = strip_media_root(path)

    return path

# used to generate custom file path
FILE_PATH = getattr_with_prefix('FILE_PATH', get_buffer_file_path)

# theme path
DEFAULT_THEME = 'default'
if 'grappelli' in settings.INSTALLED_APPS:
    DEFAULT_THEME = 'grappelli'
THEME = getattr_with_prefix('THEME', DEFAULT_THEME)

if django.get_version() >= '1.7':
    # additional processor for import and export to register
    PROCESSORS = getattr_with_prefix('PROCESSORS', [
        'mtr.sync.api.processors.xlsx',
        'mtr.sync.api.processors.xls',
        'mtr.sync.api.processors.ods',
        'mtr.sync.api.processors.csv'
    ])
else:
    # additional processor for import and export to register
    PROCESSORS = getattr_with_prefix('PROCESSORS', [
        'mtr_sync.api.processors.xlsx',
        'mtr_sync.api.processors.xls',
        'mtr_sync.api.processors.ods',
        'mtr_sync.api.processors.csv'
    ])

# default processor
DEFAULT_PROCESSOR = getattr_with_prefix('DEFAULT_PROCESSOR', 'XlsxProcessor')

# model attribute where settings placed
MODEL_SETTINGS_NAME = getattr_with_prefix(
    'MODEL_SETTINGS_NAME', 'sync_settings')

# limit preview of data on settings page
LIMIT_PREVIEW = getattr_with_prefix('LIMIT_PREVIEW', 20)

# register models at admin for debugging
REGISTER_IN_ADMIN = getattr_with_prefix('REGISTER_IN_ADMIN', True)
