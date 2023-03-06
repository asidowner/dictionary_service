import datetime
from typing import Union

from django.contrib import admin
from django.db.models import (  # noqa: WPS347
    F,
    FilteredRelation,
    OuterRef,
    Q,
    Subquery,
)
from django.utils.html import format_html_join
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from server.apps.dictionaries import models

_HTML_LIST_TEMPLATE = '<li>{}</li>'  # noqa: P103


@admin.register(models.Dictionary)
class DictionaryAdmin(admin.ModelAdmin[models.Dictionary]):
    list_display = ('id', 'code', 'name', 'current_version', 'start_date')
    readonly_fields = ('show_versions',)

    @admin.display(description=_("Dictionary version's"))
    def show_versions(self, dictionary: models.Dictionary) -> str:
        versions_qs = dictionary.dictionaryversion_set.order_by('date').all()
        return format_html_join(
            '\n',
            _HTML_LIST_TEMPLATE,
            ((version,) for version in versions_qs),
        )

    @admin.display(description=_('Current version'))
    def current_version(self, dictionary) -> Union[str, None]:
        return dictionary.version

    @admin.display(description=_('Version start date'))
    def start_date(self, dictionary) -> Union[datetime.date, None]:
        return dictionary.date

    def get_queryset(self, request):
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
    # FIXME
    model = models.DictionaryElement


@admin.register(models.DictionaryVersion)
class DictionaryVersionAdmin(admin.ModelAdmin[models.DictionaryVersion]):
    list_display = ('dictionary_id', 'dictionary_name', 'version', 'date')
    list_display_links = ('version',)
    inlines = [DictionaryElementInlines]

    @admin.display(description=_('Dictionary identifier'))
    def dictionary_id(self, version: models.DictionaryVersion) -> int:
        return version.dictionary.id

    @admin.display(description=_('Dictionary name'))
    def dictionary_name(self, version: models.DictionaryVersion) -> str:
        return version.dictionary.name

    def get_queryset(self, request):
        return super().get_queryset(
            request,
        ).select_related('dictionary')


@admin.register(models.DictionaryElement)
class DictionaryElementAdmin(admin.ModelAdmin[models.DictionaryElement]):
    list_display = (
        'id',
        'version',
        'code',
        'value',
    )
