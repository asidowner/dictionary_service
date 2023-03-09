from django.db.models import QuerySet
from django.utils.timezone import now

from server.apps.dictionaries import filters as filter_sets
from server.apps.dictionaries.models import Dictionary, DictionaryElement, DictionaryVersion


def dictionary_list(*, filters=None) -> QuerySet[Dictionary]:
    """Function for select dictionary list with filters."""
    filters = filters or {}

    qs = Dictionary.objects.all()

    return filter_sets.DictionaryFilter(filters, qs).qs


def dictionary_version_list(*, dictionary_id: int, version=None) -> QuerySet[DictionaryVersion]:
    """Function for select dictionary versions. With empty version selected with filter by date==now()."""
    filters = {'version': version} if version else {'date': now()}

    qs = DictionaryVersion.objects.filter(
        dictionary_id=dictionary_id,
    ).order_by('-date')

    return filter_sets.DictionaryVersionFilter(filters, qs).qs


def dictionary_element_list(*, dictionary_id: int, filters=None) -> QuerySet[DictionaryElement]:
    """Function for select dictionary elements. With empty filters selected with filter by current version."""
    filters = filters or {}

    qs: QuerySet[DictionaryElement] = DictionaryElement.objects.all()

    version = filters.get('version')

    if version:
        qs = qs.filter(
            version__version=version,
            version__dictionary_id=dictionary_id,
        )
    else:
        current_version_qs = dictionary_version_list(
            dictionary_id=dictionary_id,
            version=version,
        )
        qs = qs.filter(version=current_version_qs[:1])

    return filter_sets.DictionaryElementFilter(filters, qs).qs
