from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

app_name = 'censustest'

urlpatterns = [
	url(r'^get_next_topic/(?P<sequence_num>[0-9]+)/$', views.get_next_topic, name='get_next_topic'),
	url(r'^(?P<sequence_num>[0-9]+)/$', views.TopicView.as_view(), name='topic'),
	url(r'^results/$', views.ResultsView.as_view(), name='results'),
]
