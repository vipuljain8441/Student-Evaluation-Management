from rest_framework import serializers
from .models import customrole,CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
       model = CustomUser
       fields= '__all__'
       extra_kwargs = {
            'password': {'write_only': True}  
        }
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        validate_password(data['password'])
        data.pop('confirm_password', None)

        return data
    def create(self,validated_data):
        # print(self.validated_data)
        user = CustomUser.objects.create_user(**validated_data)
        # password = validated_data.pop['password']
        user.save()
        return user
    
class LoginSerializer(serializers.ModelSerializer):
    class Meta:  
        model = get_user_model()
        fields = ['email','password']
        extra_kwargs = {'password': {'write_only': True}}
        error_messages = {
            'email': {'required': 'Email is required for login.'},
            'password': {'required': 'Password is required for login.'}
        }
