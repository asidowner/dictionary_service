from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status, views
from rest_framework.response import Response

from server.apps.dictionaries import selectors
from server.apps.dictionaries.serializers import (
    DictionaryElementSerializer,
    DictionarySerializer,
)


class DictionaryListApi(views.APIView):
    class DictionaryListFilterSerializer(serializers.Serializer):
        date = serializers.DateField(required=False)

    class DictionaryOutputSerializer(serializers.Serializer):
        refbooks = DictionarySerializer(many=True)

    @extend_schema(
        parameters=[DictionaryListFilterSerializer],
        responses={
            status.HTTP_200_OK: DictionaryOutputSerializer,
        },
    )
    def get(self, request) -> Response:
        filters_serializer = self.DictionaryListFilterSerializer(
            data=request.query_params,
        )
        filters_serializer.is_valid(raise_exception=True)

        dictionaries = selectors.dictionary_list(
            filters=filters_serializer.validated_data,
        )

        output = {'refbooks': dictionaries}
        output_serializer = self.DictionaryOutputSerializer(output)
        return Response(output_serializer.data)


class DictionaryElementListApi(views.APIView):
    class DictionaryElementListFilterSerializer(serializers.Serializer):
        version = serializers.CharField(required=False)

    class DictionaryElementListOutputSerializer(serializers.Serializer):
        elements = DictionaryElementSerializer(many=True)

    @extend_schema(
        parameters=[DictionaryElementListFilterSerializer],
        responses={
            status.HTTP_200_OK: DictionaryElementListOutputSerializer,
        },
    )
    def get(self, request, dictionary_id: int):
        filters_serializer = self.DictionaryElementListFilterSerializer(
            data=request.query_params,
        )
        filters_serializer.is_valid(raise_exception=True)

        filters = filters_serializer.validated_data

        if not filters:
            version_obj = selectors.get_dictionary_current_version(
                dictionary_id=dictionary_id,
            )
            version = getattr(version_obj, 'version', None)

            if not version:
                return Response({'elements': []})

            filters['version'] = version

        elements = selectors.dictionary_element_list(
            dictionary_id=dictionary_id,
            filters=filters,
        )

        output = {'elements': elements}
        output_serializer = self.DictionaryElementListOutputSerializer(output)
        return Response(output_serializer.data)


class DictionaryCheckElementApi(views.APIView):
    class DictionaryCheckElementFilterSerializer(serializers.Serializer):
        code = serializers.CharField()
        value = serializers.CharField()  # noqa: WPS110
        version = serializers.CharField(required=False)

    @extend_schema(
        parameters=[DictionaryCheckElementFilterSerializer],
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_404_NOT_FOUND: None,
        },
    )
    def get(self, request, dictionary_id: int):
        filters_serializer = self.DictionaryCheckElementFilterSerializer(
            data=request.query_params,
        )
        filters_serializer.is_valid(raise_exception=True)

        filters = filters_serializer.validated_data

        if not filters.get('version'):
            version_obj = selectors.get_dictionary_current_version(
                dictionary_id=dictionary_id,
            )
            version = getattr(version_obj, 'version', None)

            if not version:
                return Response(status=status.HTTP_404_NOT_FOUND)

        elements = selectors.dictionary_element_list(
            dictionary_id=dictionary_id,
            filters=filters_serializer.validated_data,
        )

        if elements.exists():
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
