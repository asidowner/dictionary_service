from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DictionariesConfig(AppConfig):
    """Application provide api for work with dictionaries."""

    name = 'server.apps.dictionaries'
    verbose_name = _('Dictionaries')
