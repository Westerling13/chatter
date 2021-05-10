from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from profiles.user import User


class UserCreateSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def validate(self, validated_data):
        if validated_data['password1'] != validated_data['password2']:
            raise ValidationError('Пароли не совпадают')

        return validated_data

    def create(self, validated_data):
        instance = self.Meta.model(username=validated_data['username'])
        instance.set_password(validated_data['password1'])
        instance.save()

        return instance
