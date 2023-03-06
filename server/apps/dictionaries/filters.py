import django_filters


class DictionaryFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(
        field_name='dictionaryversion__date',
        lookup_expr='lte',
    )


class DictionaryVersionFilter(django_filters.FilterSet):
    version = django_filters.CharFilter()
    date = django_filters.DateFilter(
        field_name='date',
        lookup_expr='lte',
    )


class DictionaryElementFilter(django_filters.FilterSet):
    code = django_filters.CharFilter()
    value = django_filters.CharFilter()  # noqa: WPS110
    version = django_filters.CharFilter(field_name='version__version')
