from .models import User
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

class UserCreationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length = 25)
    email = serializers.EmailField(max_length= 80)
    phone_num = PhoneNumberField(allow_null = False, allow_blank=False)
    password = serializers.CharField(min_length = 8, write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "phone_num", "password"]
    
    def validate(self, attrs):
        username_exists = User.objects.filter(email=attrs['username']).exists()
        if username_exists:
            raise serializers.ValidationError(detail = "User with Username already exists")
        email_exists = User.objects.filter(email=attrs['email']).exists()
        if email_exists:
            raise serializers.ValidationError(detail = "User with email already exists")
        phone_number_exists = User.objects.filter(email=attrs['phone_num']).exists()
        if phone_number_exists:
            raise serializers.ValidationError(detail = "User with phone number already exists")
    
        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.create(
            email = validated_data['email'],
            username = validated_data['username'],
            phone_num = validated_data['phone_num']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user