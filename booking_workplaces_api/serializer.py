from rest_framework import serializers

from booking_workplaces_api.models import Workplace


class WorkplaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workplace
        fields = '__all__'
