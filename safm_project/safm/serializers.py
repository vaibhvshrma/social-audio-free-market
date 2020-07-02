from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import *

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    def create(self, validated_data):
        password_min_length = 8

        # Password min length validation
        if len(validated_data['password']) < password_min_length:
            raise serializers.ValidationError('Password length must be at least {0} characters.'.format(password_min_length))

        # Confirm password validation
        if validated_data['password'] != validated_data['password_confirm']:
            raise serializers.ValidationError('Password confirmation does not match.')

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        UserProfile.objects.create(user=user)

        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password_confirm']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField()
        
    def validate(self, data):
        username = ''
        if 'username' in data:
            username = data['username']
        elif 'email' in data:
            try:
                username = User.objects.get(email=data['email']).username
            except User.DoesNotExist:
                username = ''

        user = authenticate(username=username, password=data['password'])

        if user:
            return user

        raise serializers.ValidationError('Wrong credentials')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class SampleForkSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Sample
        fields = '__all__'


class SampleSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, required=False)
    forks = SampleForkSerializer( many=True, required=False)

    def create(self, validated_data):
        sample = Sample.objects.create(**validated_data)

        sample.deduce_properties()
        sample.save()

        return sample

    class Meta:
        model = Sample
        fields = '__all__'


class UserDownloadSerializer(serializers.ModelSerializer):
    sample = SampleSerializer()

    class Meta:
        model = UserSampleDownload
        fields = '__all__'
        

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = '__all__'
