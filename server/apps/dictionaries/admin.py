import datetime
from typing import Union

from django.contrib import admin
from django.db.models import F, FilteredRelation, OuterRef, Q, Subquery  # noqa: WPS347
from django.utils.html import format_html_join
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from server.apps.dictionaries import models

_HTML_LIST_TEMPLATE = '<li>{}</li>'  # noqa: P103


@admin.register(models.Dictionary)
class DictionaryAdmin(admin.ModelAdmin[models.Dictionary]):
    """Register dictionary model editor with additional information about current version."""

    list_display = ('dictionary_id', 'code', 'name', 'current_version', 'start_date')
    readonly_fields = ('show_versions',)

    @admin.display(description=_('Identifier'))
    def dictionary_id(self, dictionary: models.Dictionary) -> int:
        """Return id with custom description."""
        return dictionary.id

    @admin.display(description=_("Dictionary version's"))
    def show_versions(self, dictionary: models.Dictionary) -> str:
        """Return dictionary version list on edit form."""
        versions_qs = dictionary.dictionaryversion_set.order_by('date').all()
        return format_html_join(
            '\n',
            _HTML_LIST_TEMPLATE,
            ((version,) for version in versions_qs),
        )

    @admin.display(description=_('Current version'))
    def current_version(self, dictionary) -> Union[str, None]:
        """Return current version."""
        return dictionary.version

    @admin.display(description=_('Version start date'))
    def start_date(self, dictionary) -> Union[datetime.date, None]:
        """Return start date of current version."""
        return dictionary.date

    def get_queryset(self, request):
        """Override method for additional information about current version."""
        current_versions_sq = Subquery(
            (
                models.DictionaryVersion.objects.filter(
                    dictionary_id=OuterRef('pk'),
                    date__lte=now(),
                ).order_by('-date').values('id')[:1]
            ),
        )

        return super().get_queryset(request).annotate(
            currentversion=FilteredRelation(
                'dictionaryversion',
                condition=Q(dictionaryversion=current_versions_sq),
            ),
            version=F('currentversion__version'),
            date=F('currentversion__date'),
        )


class DictionaryElementInlines(admin.StackedInline):  # type: ignore[type-arg]
    """Forms for add elements on dictionary version admin edit form."""

    model = models.DictionaryElement


@admin.register(models.DictionaryVersion)
class DictionaryVersionAdmin(admin.ModelAdmin[models.DictionaryVersion]):
    """Register dictionary version model editor with dictionary elements inlines."""

    list_display = ('version', 'dictionary_identifier', 'dictionary_name', 'date')
    inlines = [DictionaryElementInlines]

    @admin.display(description=_('Dictionary identifier'))
    def dictionary_identifier(self, version: models.DictionaryVersion) -> int:
        """Return dictionary id."""
        return version.dictionary.id

    @admin.display(description=_('Dictionary name'))
    def dictionary_name(self, version: models.DictionaryVersion) -> str:
        """Return dictionary name."""
        return version.dictionary.name


@admin.register(models.DictionaryElement)
class DictionaryElementAdmin(admin.ModelAdmin[models.DictionaryElement]):
    """Register dictionary element model."""

    list_display = (
        'version',
        'code',
        'value',
    )
