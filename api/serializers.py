__author__ = 'jschnall'

from django.contrib.auth.models import User
from rest_framework import serializers
from models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class CompositionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Composition
        fields = ('created', 'updated', 'owner', 'users', 'title', 'turns', 'min_part_chars', 'max_part_chars')


class PartSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Part
        fields = ('created', 'updated', 'owner', 'composition', 'text', 'segue')
