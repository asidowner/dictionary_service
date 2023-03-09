import json
from dataclasses import asdict, dataclass

from django.test import TestCase
from django.utils.timezone import now
from rest_framework.test import APIClient, APIRequestFactory

from tests.test_apps.test_dictionaries import factories


@dataclass
class DictionaryData(object):
    """Dictionary dataclass."""

    id: str
    code: str
    name: str


@dataclass
class ElementData(object):
    """Element dataclass."""

    code: str
    value: str  # noqa: WPS110


@dataclass
class ElementRequestData(object):
    """Request data for elements api dataclass."""

    code: str
    value: str  # noqa: WPS110


@dataclass
class ElementWithVersionRequestData(ElementRequestData):
    """Request data with version for elements api dataclass."""

    version: str


class TestRefbooksApi(TestCase):
    """This is api test /refbooks/."""

    def setUp(self) -> None:
        """Setup test data for test case."""
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.uri = '/refbooks/'

    def test_refbooks_api(self) -> None:
        """Tests refbooks api contain created dictionary."""
        expected_dictionary = factories.DictionaryFactory()

        response = self.client.get(self.uri)

        assert response.status_code == 200

        response_body = json.loads(response.content)

        dictionary = DictionaryData(**response_body.get('refbooks')[0])

        assert dictionary.id == str(expected_dictionary.id)
        assert dictionary.code == expected_dictionary.code
        assert dictionary.name == expected_dictionary.name

    def test_refbooks_with_three_dicts_api(self) -> None:
        """Tests refbooks api contain three created dictionaries."""
        dicts = factories.DictionaryFactory.create_batch(3)

        response = self.client.get(self.uri)
        response_body = json.loads(response.content)

        assert len(response_body.get('refbooks')) == len(dicts)

    def test_refbooks_with_future_start_date(self) -> None:  # noqa: WPS210
        """Tests refbooks api return only date filtered by date==now()."""
        future_versions = factories.DictionaryVersionWithFutureDateFactory.create_batch(3)
        current_versions = factories.DictionaryVersionWithCurrentDateFactory.create_batch(3)
        past_versions = [
            *factories.DictionaryVersionFactory.create_batch(3),
            factories.DictionaryVersionFactory(dictionary=current_versions[0].dictionary),
            factories.DictionaryVersionFactory(dictionary=future_versions[0].dictionary),
        ]

        request_data = {'date': str(now().date())}
        response = self.client.get(self.uri, data=request_data)

        response_body = json.loads(response.content)

        expected_len = len(current_versions[1:]) + len(past_versions)
        assert len(response_body.get('refbooks')) == expected_len


class TestElementsApi(TestCase):
    """This is api test /refbooks/<int:dictionary_id>/elements."""

    def setUp(self) -> None:
        """Setup test data for test case."""
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.uri = '/refbooks/{0}/elements'

    def test_elements_api(self) -> None:  # noqa: WPS210
        """Tests elements api contain created elements."""
        version = factories.DictionaryVersionFactory()
        expected_elements = factories.DictionaryElementFactory.create_batch(3, version=version)

        response = self.client.get(self.uri.format(version.dictionary.id))
        assert response.status_code == 200

        response_body = json.loads(response.content)

        elements = [ElementData(**element) for element in response_body.get('elements')]
        assert len(elements) == len(expected_elements)

        for index, element in enumerate(elements):
            assert element.code == expected_elements[index].code
            assert element.value == expected_elements[index].value

    def test_with_future_date_with_version(self) -> None:  # noqa: WPS210
        """Tests elements api contain created elements."""
        future_version = factories.DictionaryVersionWithFutureDateFactory()
        future_elements = factories.DictionaryElementFactory.create_batch(3, version=future_version)
        for future_element in future_elements:
            factories.DictionaryFactory(code=future_element.code)

        request_data = {'version': future_version.version}
        response = self.client.get(
            self.uri.format(future_version.dictionary.id),
            data=request_data,
        )
        assert response.status_code == 200

        response_body = json.loads(response.content)
        assert len(response_body.get('elements')) == len(future_elements)

        elements = [ElementData(**element) for element in response_body.get('elements')]

        for index, element in enumerate(elements):
            assert element.code == future_elements[index].code
            assert element.value == future_elements[index].value

    def test_with_future_date_without_version(self) -> None:
        """Tests elements api return empty elements."""
        version = factories.DictionaryVersionWithFutureDateFactory()
        factories.DictionaryElementFactory.create_batch(3, version=version)

        response = self.client.get(self.uri.format(version.dictionary.id))
        assert response.status_code == 200

        response_body = json.loads(response.content)
        assert not bool(response_body.get('elements'))


class TestCheckElementApi(TestCase):
    """This is api test /refbooks/<int:dictionary_id>/check_element."""

    def setUp(self) -> None:
        """Setup test data for test case."""
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.uri = '/refbooks/{0}/check_element'

    def test_check_element_api(self) -> None:
        """Tests elements api work correctly."""
        element = factories.DictionaryElementFactory()

        dictionary_id = element.version.dictionary.id
        request_data = ElementRequestData(element.code, element.value)

        response = self.client.get(
            self.uri.format(dictionary_id),
            data=asdict(request_data),
        )
        assert response.status_code == 204

    def test_check_element_with_future_date_api(self) -> None:
        """Tests elements api return only by filter version."""
        future_version = factories.DictionaryVersionWithFutureDateFactory()
        element = factories.DictionaryElementFactory(version=future_version)

        dictionary_id = future_version.dictionary.id

        request_data = ElementRequestData(element.code, element.value)
        response = self.client.get(
            self.uri.format(dictionary_id),
            data=asdict(request_data),
        )
        assert response.status_code == 404

        request_data = ElementWithVersionRequestData(element.code, element.value, element.version)
        response = self.client.get(
            self.uri.format(dictionary_id),
            data=asdict(request_data),
        )
        assert response.status_code == 204

    def test_check_element_with_three_version_api(self) -> None:  # noqa: WPS210
        """Tests elements api return only by current version."""
        past_version = factories.DictionaryVersionFactory()
        dictionary = past_version.dictionary
        current_version = factories.DictionaryVersionWithCurrentDateFactory(dictionary=dictionary)
        future_version = factories.DictionaryVersionWithFutureDateFactory(dictionary=dictionary)
        past_element = factories.DictionaryElementFactory(version=past_version)
        current_element = factories.DictionaryElementFactory(version=current_version)
        factories.DictionaryElementFactory(version=future_version)

        request_data = ElementRequestData(past_element.code, past_element.value)
        response = self.client.get(
            self.uri.format(dictionary.id),
            data=asdict(request_data),
        )
        assert response.status_code == 404

        request_data = ElementRequestData(current_element.code, current_element.value)
        response = self.client.get(
            self.uri.format(dictionary.id),
            data=asdict(request_data),
        )
        assert response.status_code == 204

    def test_with_exception(self) -> None:
        """Tests required query string params."""
        element = factories.DictionaryElementFactory()
        dictionary_id = element.version.dictionary.id

        response = self.client.get(self.uri.format(dictionary_id))
        assert response.status_code == 400

        request_data = {'code': element.code}
        response = self.client.get(
            self.uri.format(dictionary_id),
            data=request_data,
        )
        assert response.status_code == 400

        request_data = {'value': element.value}
        response = self.client.get(
            self.uri.format(dictionary_id),
            data=request_data,
        )
        assert response.status_code == 400
