from rest_framework import serializers

from server.apps.dictionaries.models import Dictionary, DictionaryElement


class DictionarySerializer(serializers.ModelSerializer):
    id = serializers.CharField()

    class Meta:
        model = Dictionary
        fields = ('id', 'code', 'name')


class DictionaryElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = DictionaryElement
        fields = ('code', 'value')
