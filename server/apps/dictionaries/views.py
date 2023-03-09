from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status, views
from rest_framework.response import Response

from server.apps.dictionaries import selectors
from server.apps.dictionaries.serializers import DictionaryElementSerializer, DictionarySerializer


class DictionaryListApi(views.APIView):
    """Dictionary list api."""

    class DictionaryListFilterSerializer(serializers.Serializer):  # noqa: WPS431
        """Dictionary list filter serializer."""

        date = serializers.DateField(required=False)

    class DictionaryOutputSerializer(serializers.Serializer):  # noqa: WPS431
        """Dictionary list output serializer."""

        refbooks = DictionarySerializer(many=True)

    @extend_schema(
        parameters=[DictionaryListFilterSerializer],
        responses={
            status.HTTP_200_OK: DictionaryOutputSerializer,
        },
    )
    def get(self, request) -> Response:
        """Return filtered dictionary list."""
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


class DictionaryElementListApi(views.APIView):
    """Dictionary elements list api."""

    class DictionaryElementListFilterSerializer(serializers.Serializer):  # noqa: WPS431
        """Dictionary elements filter serializer."""

        version = serializers.CharField(required=False)

    class DictionaryElementListOutputSerializer(serializers.Serializer):  # noqa: WPS431
        """Dictionary elements output serializer."""

        elements = DictionaryElementSerializer(many=True, required=False)

    @extend_schema(
        parameters=[DictionaryElementListFilterSerializer],
        responses={
            status.HTTP_200_OK: DictionaryElementListOutputSerializer,
        },
    )
    def get(self, request, dictionary_id: int):
        """Return elements from dictionary id."""
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


class DictionaryCheckElementApi(views.APIView):
    """Check element api."""

    class DictionaryCheckElementFilterSerializer(serializers.Serializer):  # noqa: WPS431
        """Check element api filter."""

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
        """ToDo."""
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
