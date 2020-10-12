from os import path

from django.apps import AppConfig
from django.conf import settings
from django.utils.autoreload import autoreload_started


# pylint: disable=unused-argument
def autoreload_watch(sender, **kwargs):
    """Add any Glyph-specific files to autoreload on
    """
    sender.watch_dir(path.dirname(settings.YASG_SCHEMA['DESCRIPTION_PATH']), '*.md')


class CommandsConfig(AppConfig):
    name = f'{settings.API_IMPORT_ROOT}.commands'

    def ready(self):
        autoreload_started.connect(autoreload_watch)
