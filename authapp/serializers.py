from django.contrib.auth.models import User
from rest_framework import serializers


# User serializer to make JSON of user object
class UserSerializer(serializers.HyperlinkedModelSerializer):
    
    def create(self, validated_data):
        u = User.objects.create_user(**validated_data)
        return u

    class Meta:
        model = User
        fields = ('pk', 'url', 'username', 'password', 'email', 'is_staff')

