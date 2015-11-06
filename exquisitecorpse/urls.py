__author__ = 'jschnall'

from django.conf.urls import patterns, include, url
from exquisitecorpse import views

from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers

#router = routers.SimpleRouter()
#router.register(r'parts', views.PartViewSet)
#urlpatterns = router.urls

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^compositions/$', views.CompletedCompositionList.as_view(), name='completed_composition_list'),
    url(r'^compositions/available/$', views.AvailableCompositionList.as_view(), name='available_composition_list'),
    url(r'^compositions/add/$', views.CompositionCreate.as_view(), name='composition_create'),
    url(r'^compositions/(?P<pk>\d+)/$', views.CompositionDetails.as_view(), name='composition_details'),
    url(r'^compositions/(?P<pk>\d+)/update/$', views.CompositionUpdate.as_view(), name='composition_update'),
    url(r'^compositions/(?P<pk>\d+)/delete/$', views.CompositionDelete.as_view(), name='composition_delete'),
    url(r'^compositions/(?P<pk>\d+)/add_part/$', views.PartCreate.as_view(), name='part_create'),
    url(r'^dashboard/$', views.Dashboard.as_view(), name='dashboard'),
    url(r'^dashboard/(?P<category>\w+)/$', views.Dashboard.as_view(), name='dashboard'),
    #url(r'^parts/add/$', views.PartCreate.as_view(), name='part_create'),
    url(r'^parts/(?P<pk>\d+)/$', views.PartDetails.as_view(), name='part_details'),

    #url(r'^', include(router.urls)),

    # Ajax requests
    url(r'^like_part/$', views.PartLike.as_view(), name='part_like'),
    url(r'^like_composition/$', views.CompositionLike.as_view(), name='composition_like'),
    url(r'^favorite_composition/$', views.CompositionFavorite.as_view(), name='composition_favorite'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
