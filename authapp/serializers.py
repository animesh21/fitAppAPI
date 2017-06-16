from django.contrib.auth.models import User
from rest_framework import serializers


# User serializer to make JSON of user object
class UserSerializer(serializers.HyperlinkedModelSerializer):
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.password = validated_data.get('password', instance.password)
        instance.email = validated_data.get('email', instance.password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('pk', 'url', 'username', 'password', 'email', 'is_staff')

