from django.utils.timezone import now
from django.utils.translation import gettext as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import serializers, status, views
from rest_framework.response import Response

from server.apps.dictionaries import misc, selectors
from server.apps.dictionaries.serializers import DictionaryElementSerializer, DictionarySerializer


class DictionaryListAPI(views.APIView):
    """Dictionary list apiview class."""

    class DictionaryListFilterSerializer(serializers.Serializer):  # noqa: WPS431
        """Dictionary list filter serializer."""

        def update(self, instance, validated_data):
            """Not in use."""

        def create(self, validated_data):
            """Not in use."""

        date = serializers.DateField(required=False)

    class DictionaryOutputSerializer(serializers.Serializer):  # noqa: WPS431
        """Dictionary list output serializer."""

        refbooks = DictionarySerializer(many=True)

        def update(self, instance, validated_data):
            """Not in use."""

        def create(self, validated_data):
            """Not in use."""

    @extend_schema(
        summary=misc.DICTIONARY_LIST_API_SUMMARY,
        description=misc.DICTIONARY_LIST_API_DESCRIPTION,
        parameters=[
            OpenApiParameter(
                name='date',
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description=misc.DATE_QUERY_PARAM_DESCRIPTION,
                examples=[
                    OpenApiExample(
                        str(_('Example with current date')),
                        summary=str(_('Current date')),
                        value=now().date(),
                    ),
                ],
            ),
        ],
        responses={
            status.HTTP_200_OK: DictionaryOutputSerializer,
        },
        examples=[
            OpenApiExample(
                str(_('Example successful response')),
                response_only=True,
                status_codes=[status.HTTP_200_OK],
                value="""
                {
                  "refbooks": [
                    {
                      "id": "1",
                      "code": "Dict1",
                      "name": "Dict1_name"
                    },
                    {
                      "id": "2",
                      "code": "Dict2",
                      "name": "Dict2_name"
                    }
                  ]
                }
                """),
            OpenApiExample(
                str(_('Example response if dictionary not found')),
                value='{"refbooks": []}',
                response_only=True,
                status_codes=[status.HTTP_200_OK],
            ),
        ],
    )
    def get(self, request) -> Response:
        """Obtaining a list of dictionaries."""
        filters_serializer = self.DictionaryListFilterSerializer(
            data=request.query_params,
        )
        filters_serializer.is_valid(raise_exception=True)

        dictionaries = selectors.dictionary_list(
            filters=filters_serializer.validated_data,
        ).distinct()

        output = {'refbooks': dictionaries}
        output_serializer = self.DictionaryOutputSerializer(output)
        return Response(output_serializer.data)


class DictionaryElementListAPI(views.APIView):
    """Dictionary elements list api."""

    class DictionaryElementListFilterSerializer(serializers.Serializer):  # noqa: WPS431
        """Dictionary elements filter serializer."""

        version = serializers.CharField(required=False)

        def update(self, instance, validated_data):
            """Not in use."""

        def create(self, validated_data):
            """Not in use."""

    class DictionaryElementListOutputSerializer(serializers.Serializer):  # noqa: WPS431
        """Dictionary elements output serializer."""

        def update(self, instance, validated_data):
            """Not in use."""

        def create(self, validated_data):
            """Not in use."""

        elements = DictionaryElementSerializer(many=True, required=False)

    @extend_schema(
        summary=misc.ELEMENTS_LIST_API_SUMMARY,
        description=misc.ELEMENTS_LIST_API_DESCRIPTION,
        parameters=[
            OpenApiParameter(
                name='dictionary_id',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description=misc.DICTIONARY_ID_PATH_PARAM_DESCRIPTION,
                required=True,
                examples=[
                    OpenApiExample(
                        str(_('Example dictionary id')),
                        value='1',
                    ),
                ],
            ),
            OpenApiParameter(
                name='version',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description=misc.VERSION_QUERY_PARAM_DESCRIPTION,
                examples=[
                    OpenApiExample(
                        str(_('Example version')),
                        value='vers_2',
                    ),
                ],
            ),
        ],
        responses={
            status.HTTP_200_OK: DictionaryElementListOutputSerializer,
        },
        examples=[
            OpenApiExample(
                str(_('Example successful response')),
                response_only=True,
                status_codes=[status.HTTP_200_OK],
                value="""
                {
                  "elements": [
                    {
                      "code": "element_111",
                      "value": "value_111"
                    },
                    {
                      "code": "element_222",
                      "value": "value_222"
                    }
                  ]
                }
                """),
            OpenApiExample(
                str(_('Example response if elements not found')),
                value='{"elements": []}',
                response_only=True,
                status_codes=[status.HTTP_200_OK],
            ),
        ],
    )
    def get(self, request, dictionary_id: int):
        """Retrieving items from a given dictionaries."""
        filters_serializer = self.DictionaryElementListFilterSerializer(
            data=request.query_params,
        )
        filters_serializer.is_valid(raise_exception=True)

        elements = selectors.dictionary_element_list(
            dictionary_id=dictionary_id,
            filters=filters_serializer.validated_data,
        )

        output = {'elements': elements}
        output_serializer = self.DictionaryElementListOutputSerializer(output)
        return Response(output_serializer.data)


class DictionaryCheckElementAPI(views.APIView):
    """Check element api."""

    class DictionaryCheckElementFilterSerializer(serializers.Serializer):  # noqa: WPS431
        """Check element api filter."""

        code = serializers.CharField()
        value = serializers.CharField()  # noqa: WPS110
        version = serializers.CharField(required=False)

        def update(self, instance, validated_data):
            """Not in use."""

        def create(self, validated_data):
            """Not in use."""

    @extend_schema(
        summary=misc.ELEMENTS_CHECK_API_SUMMARY,
        description=misc.ELEMENTS_CHECK_API_DESCRIPTION,
        parameters=[
            OpenApiParameter(
                name='dictionary_id',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description=misc.DICTIONARY_ID_PATH_PARAM_DESCRIPTION,
                required=True,
                examples=[
                    OpenApiExample(
                        str(_('Example dictionary id')),
                        value='1',
                    ),
                ],
            ),
            OpenApiParameter(
                name='code',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description=misc.CODE_QUERY_PARAM_DESCRIPTION,
                required=True,
                examples=[
                    OpenApiExample(
                        str(_('Example code')),
                        value='element_111',
                    ),
                ],
            ),
            OpenApiParameter(
                name='value',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description=misc.VALUE_QUERY_PARAM_DESCRIPTION,
                required=True,
                examples=[
                    OpenApiExample(
                        str(_('Example value')),
                        value='value_111',
                    ),
                ],
            ),
            OpenApiParameter(
                name='version',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description=misc.VERSION_QUERY_PARAM_DESCRIPTION,
                examples=[
                    OpenApiExample(
                        str(_('Example version')),
                        value='vers_2',
                    ),
                ],
            ),
        ],
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(description='Validation done.'),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description='Validation not preformed.'),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description='Required query params not found.',
                examples=[
                    OpenApiExample(
                        str(_('Example response if required params are not passed')),
                        value="""
                        {
                            "message": "Validation error",
                            "extra": {
                                "fields": {
                                    "code": [
                                        "Обязательное поле."
                                    ],
                                    "value": [
                                        "Обязательное поле."
                                    ]
                                }
                            }
                        }
                        """,
                        response_only=True,
                        status_codes=[status.HTTP_400_BAD_REQUEST],
                    ),
                ],
            ),
        },
    )
    def get(self, request, dictionary_id: int):
        """Validation an element."""
        filters_serializer = self.DictionaryCheckElementFilterSerializer(
            data=request.query_params,
        )
        filters_serializer.is_valid(raise_exception=True)

        elements = selectors.dictionary_element_list(
            dictionary_id=dictionary_id,
            filters=filters_serializer.validated_data,
        )

        if not elements.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)
