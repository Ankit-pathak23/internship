# serializers.py

from rest_framework import serializers
from .models import Device, TemperatureReading, HumidityReading

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['uid', 'name']

class TemperatureReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemperatureReading
        fields = ['temperature', 'timestamp']

class HumidityReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = HumidityReading
        fields = ['humidity', 'timestamp']

# class TemperatureAndCorrespondigHumidity()
