__author__ = 'jschnall'

from django.contrib.auth.models import User
from rest_framework import viewsets
from serializers import *

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLogin

# Social Authentication
class FacebookLogin(SocialLogin):
    adapter_class = FacebookOAuth2Adapter

#class GoogleSignIn(SocialLogin):
#    adapter_class = GoogleOauth2Adapter

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CompositionViewSet(viewsets.ModelViewSet):
    queryset = Composition.objects.all()
    serializer_class = CompositionSerializer


class PartViewSet(viewsets.ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer