from rest_framework import serializers
from .models import *

class DigitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Digital
        fields ="__all__"
        
class AnalogSerializer( serializers.ModelSerializer):
        
    class Meta:
        model = Analog
        fields = "__all__"