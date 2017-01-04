from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.urls import reverse
from chartit import DataPool, Chart

from .models import Choice, Question, Topic


class TestView(generic.ListView):
	model = Topic
	template_name = 'censustest/test.html'


def save_answers(request):
	has_error = False
	error_msg = ""
	for topic in Topic.objects.all():
		for question in topic.question_set.all():
			question_key = 'question%d' % (question.id)
			if question_key not in request.POST:
				continue

			choices = [int(choice) for choice in request.POST.getlist(question_key)]
			request.session[str(question.id)] = choices

	return HttpResponseRedirect(reverse('censustest:results'))


class ResultsView(generic.ListView):
	model = Topic
	template_name = 'censustest/results.html'

	def get_context_data(self, **kwargs):
		context = super(ResultsView, self).get_context_data(**kwargs)
		charts = []
		chart_div_ids = []
		stats_dict = {}
		for topic in self.get_queryset():
			for question in topic.question_set.all():
				choices = self.request.session.get(str(question.id), default=[])
				charts.append(get_chart(question, choices))
				chart_div_ids.append('chart_%d' % (question.id))
				stats_dict[question.id] = question.get_stats(choices)
		context['charts'] = charts
		context['chart_div_ids'] = ','.join(chart_div_ids)
		context['stats_dict'] = stats_dict

		self.request.session.clear()

		return context

def get_chart(question, choices):
	dp = DataPool(
	   series=
		[{'options': {
		   'source': question.get_chart_data(choices)},
		  'terms': [
			'text',
			'response_percent']}
		 ])

	cht = Chart(
		datasource = dp,
		series_options =
		  [{'options':{
			  'type': 'column',
			  'stacking': False},
			'terms':{
			  'text': [
				'response_percent']
			  }}],
		chart_options =
		  {'title': {
			   'text': question.title},
		   'xAxis': {
				'title': {
				   'text': 'Choice'}},
			'yAxis': {
				 'title': {
					'text': 'Response Percent'}},
			'legend': {
				'enabled': False},
			'tooltip': {
				'pointFormat': "{point.y:.1f}%"},
			'plotOptions': {
				'series': {
					'color': '#d9534f'}}})

	return cht
