from rest_framework import serializers

from booking_workplaces_api.models import Workplace
from booking_workplaces_api.views import BookingWorkplace


class WorkplaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workplace
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    workplace = WorkplaceSerializer(many=False, read_only=True)

    class Meta:
        model = BookingWorkplace
        fields = ("description", "workplace", "datetime_from", "datetime_to")
