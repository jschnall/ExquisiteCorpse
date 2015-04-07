__author__ = 'jschnall'

from django.conf.urls import patterns, include, url
from rest_framework import routers
from api.views import *

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.include_root_view = True
router.register(r'users', UserViewSet)
router.register(r'compositions', CompositionViewSet)
router.register(r'parts', PartViewSet)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^/rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),
    #url(r'^/rest-auth/google/$', GoogleSignIn.as_view(), name='google_signin'),
)
