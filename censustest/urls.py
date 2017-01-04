from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

app_name = 'censustest'

urlpatterns = [
	url(r'^test/$', views.TestView.as_view(), name='test'),
	url(r'^save_answers/$', views.save_answers, name='save_answers'),
	url(r'^results/$', views.ResultsView.as_view(), name='results'),
]
