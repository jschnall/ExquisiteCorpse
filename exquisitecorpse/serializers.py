__author__ = 'jschnall'

from django.contrib.auth.models import User
from rest_framework import serializers
from api.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class CompositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Composition
        fields = ('created', 'updated', 'owner', 'users', 'title', 'rounds', 'min_part_chars', 'max_part_chars')


class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = ('created', 'updated', 'owner', 'composition', 'text', 'segue')
