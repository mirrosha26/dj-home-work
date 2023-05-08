from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        if self.initial_data.get('status') == 'CLOSED':
            return data
        request = self.context["request"]
        advertisements_count = Advertisement.objects.filter(status='OPEN', creator=request.user).count()
        if request.method in ['POST', 'PUT', 'PATCH'] and advertisements_count >= 10:
            raise serializers.ValidationError('Превышено количество открытых объявлений', code='invalid')
        return data