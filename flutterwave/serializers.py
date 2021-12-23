from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only= True
    )

    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'phone']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class ViewAllUsers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'is_premium', 'is_superuser']