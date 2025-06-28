from rest_framework import serializers
from my_app.models import Worker, CheckIn


class CheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckIn
        fields = '__all__'
        extra_kwargs = {
            "worker": {"read_only": True},
        }


class WorkerSerializer(serializers.ModelSerializer):
    checkins = CheckInSerializer(many=True, read_only=True)

    class Meta:
        model = Worker
        fields = ['id', 'telegram_id', 'username', 'first_name', 'last_name', 'language', 'checkins']
