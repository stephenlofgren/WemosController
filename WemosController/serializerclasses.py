"""defines serializers for data models"""
from django.contrib.auth.models import User
from rest_framework import serializers
from Base.models import D1Mini, D1MiniCommand, D1MiniEvent, D1MiniReading


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    """defines the fields that will be serialized into json"""
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class D1MiniSerializer(serializers.HyperlinkedModelSerializer):
    """defines the fields that will be serialized into json"""
    class Meta:
        model = D1Mini
        fields = ('id', 'mac_id', 'alias', 'has_dht', 'url')


class D1MiniCommandSerializer(serializers.HyperlinkedModelSerializer):
    """defines the fields that will be serialized into json"""
    class Meta:
        model = D1MiniCommand
        fields = ('pk', 'device', 'pin_id', 'pin_mode',
                  'pin_level', 'date_command', 'acknowledged')


class D1MiniEventSerializer(serializers.HyperlinkedModelSerializer):
    """defines the fields that will be serialized into json"""
    class Meta:
        model = D1MiniEvent
        fields = ('pk', 'device', 'PinID', 'PinMode', 'PinLevel',
                  'DateCommand', 'Acknowledged')


class D1MiniReadingSerializer(serializers.HyperlinkedModelSerializer):
    """defines the fields that will be serialized into json"""
    class Meta:
        model = D1MiniReading
        fields = ('pk', 'device', 'reading_type', 'reading_value',
                  'reading_unit', 'date_reading')


