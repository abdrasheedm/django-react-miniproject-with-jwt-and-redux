# from django.contrib.auth.password_validation import validate_password
# from django.core import exceptions
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validate_data):
        user = User.objects.create_user(
            first_name = validate_data['first_name'],
            last_name = validate_data['last_name'],
            email = validate_data['email'],
            password = validate_data['password']
        )

        return user



class  LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'password')
        