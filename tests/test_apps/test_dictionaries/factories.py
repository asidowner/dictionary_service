import factory
from django.utils.timezone import now

from server.apps.dictionaries import models
from tests.utils.base import faker


class DictionaryFactory(factory.django.DjangoModelFactory):
    """This is factory for generate Dictionary model."""

    class Meta:  # noqa: WPS306
        model = models.Dictionary

    code = factory.LazyAttribute(
        lambda _: faker.unique.pystr(
            min_chars=10,
            max_chars=models.DICTIONARY_CODE_MAX_LENGTH,
        ),
    )
    name = factory.LazyAttribute(
        lambda _: faker.unique.pystr(
            min_chars=10,
            max_chars=models.DICTIONARY_NAME_MAX_LENGTH,
        ),
    )
    description = factory.LazyAttribute(lambda _: faker.unique.pystr())


class DictionaryVersionFactory(factory.django.DjangoModelFactory):
    """This is factory for generate DictionaryVersion model."""

    class Meta:  # noqa: WPS306
        model = models.DictionaryVersion

    dictionary = factory.SubFactory(DictionaryFactory)
    version = factory.LazyAttribute(
        lambda _: faker.unique.pystr(
            min_chars=10,
            max_chars=models.DICTIONARY_VERSION_VERSION_MAX_LENGTH,
        ),
    )
    date = factory.LazyAttribute(lambda _: faker.unique.past_date())


class DictionaryVersionWithCurrentDateFactory(DictionaryVersionFactory):
    """This is factory for generate DictionaryVersion model with date == now()."""

    date = now()


class DictionaryVersionWithFutureDateFactory(DictionaryVersionFactory):
    """This is factory for generate DictionaryVersion model with date at future."""

    date = factory.LazyAttribute(lambda _: faker.unique.future_date())


class DictionaryElementFactory(factory.django.DjangoModelFactory):
    """This is factory for generate DictionaryElement model."""

    class Meta:  # noqa: WPS306
        model = models.DictionaryElement

    version = factory.SubFactory(DictionaryVersionFactory)
    code = factory.LazyAttribute(
        lambda _: faker.unique.pystr(
            min_chars=10,
            max_chars=models.DICTIONARY_ELEMENT_CODE_MAX_LENGTH,
        ),
    )
    value = factory.LazyAttribute(  # noqa: WPS110
        lambda _: faker.unique.pystr(
            min_chars=10,
            max_chars=models.DICTIONARY_ELEMENT_VALUE_MAX_LENGTH,
        ),
    )
