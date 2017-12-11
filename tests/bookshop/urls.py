from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^authors/$', views.AuthorCreateView.as_view(), name='author_create'),
    url(r'^authors/(?P<pk>[0-9]+)/$', views.AuthorDetailView.as_view(), name='author_details'),
    url(r'^authors/(?P<pk>[0-9]+)/update/$', views.AuthorUpdateView.as_view(), name='author_update'),
]
