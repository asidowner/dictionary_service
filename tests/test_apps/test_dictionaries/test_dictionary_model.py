import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase

from server.apps.dictionaries import models
from tests.test_apps.test_dictionaries import factories


class TestDictionary(TestCase):
    """This is a property-based test that ensures model correctness."""

    def test_model_properties(self) -> None:
        """Tests that instance can be saved and has correct representation."""
        dictionary: models.Dictionary = factories.DictionaryFactory.build()

        dictionary.save()

        assert dictionary.id > 0
        assert len(str(dictionary)) <= models.DICTIONARY_NAME_MAX_LENGTH

    def test_model_code_unique(self) -> None:
        """Tests second instance can't save with same code."""
        first = factories.DictionaryFactory()
        second = factories.DictionaryFactory.build(code=first.code)

        with pytest.raises(ValidationError):
            second.full_clean()


class TestDictionaryVersion(TestCase):
    """This is a property-based test that ensures model correctness."""

    def test_model_properties(self) -> None:
        """Tests that instance can be saved and has correct representation."""
        version = factories.DictionaryVersionFactory()

        assert version.id > 0
        assert len(str(version)) <= models.DICTIONARY_VERSION_VERSION_MAX_LENGTH

    def test_unique_version_dictionary_id(self) -> None:
        """Tests second instance can't save with same version and dictionary_id."""
        first = factories.DictionaryVersionFactory()
        second = factories.DictionaryVersionFactory.build(version=first.version, dictionary=first.dictionary)

        with pytest.raises(ValidationError):
            second.full_clean()

    def test_unique_version_date_dictionary(self):
        """Tests second instance can't save with same date and dictionary_id."""
        first = factories.DictionaryVersionFactory()
        second = factories.DictionaryVersionFactory.build(date=first.date, dictionary=first.dictionary)

        with pytest.raises(ValidationError):
            second.full_clean()


class TestDictionaryElement(TestCase):
    """This is a property-based test that ensures model correctness."""

    def test_model_properties(self) -> None:
        """Tests that instance can be saved and has correct representation."""
        element = factories.DictionaryElementFactory()

        assert element.id > 0
        assert len(str(element)) <= models.DICTIONARY_ELEMENT_CODE_MAX_LENGTH

    def test_unique_code_version_id(self):
        """Tests second instance can't save with same code and version."""
        first = factories.DictionaryElementFactory()
        second = factories.DictionaryElementFactory.build(code=first.code, version=first.version)

        with pytest.raises(ValidationError):
            second.full_clean()
