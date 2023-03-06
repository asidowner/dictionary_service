from typing import Optional

from django.db.models import QuerySet
from django.utils.timezone import now

from server.apps.dictionaries import filters as filter_sets
from server.apps.dictionaries.models import (
    Dictionary,
    DictionaryElement,
    DictionaryVersion,
)


def get_dictionary_current_version(*, dictionary_id: int) -> Optional[DictionaryVersion]:
    return DictionaryVersion.objects.filter(
        dictionary_id=dictionary_id,
        date__lte=now(),
    ).order_by('-date').only('version').first()


def dictionary_list(*, filters=None) -> QuerySet[Dictionary]:
    filters = filters or {}

    qs = Dictionary.objects.all()

    return filter_sets.DictionaryFilter(filters, qs).qs.distinct()


def dictionary_element_list(*, dictionary_id: int, filters=None) -> QuerySet[DictionaryElement]:
    filters = filters or {}
    qs = DictionaryElement.objects.filter(
        version__dictionary_id=dictionary_id,
    ).all()

    return filter_sets.DictionaryElementFilter(filters, qs).qs
