from django.contrib.auth.models import User
from rest_framework import serializers


# User serializer to make JSON of user object
class UserSerializer(serializers.HyperlinkedModelSerializer):

    password = serializers.CharField(required=False)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.get('password', '')
        if instance.check_password(raw_password=password):
            instance.set_password(raw_password=password)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('pk', 'url', 'username', 'password', 'email', 'is_staff')

