from rest_framework import serializers
from .models import Senior


class SeniorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Senior
        fields = ('id', 'name', 'position', 'greeting', 'created_by')
