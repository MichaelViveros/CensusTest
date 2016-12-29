from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.urls import reverse
from chartit import DataPool, Chart

from .models import Choice, Question, Topic


class TopicView(generic.DetailView):
	model = Topic
	template_name = 'censustest/topic.html'
	slug_url_kwarg = 'sequence_num'
	slug_field = 'sequence_num'


def get_next_topic(request, sequence_num):
	num_topics = Topic.objects.count()

	if int(sequence_num) < 0 or int(sequence_num) > num_topics:
		return HttpResponseRedirect(reverse('censustest:index'))
	elif int(sequence_num) != 0:
		has_error = False
		error_msg = ""
		topic = Topic.objects.get(sequence_num=sequence_num)
		for question in topic.question_set.all():
			question_key = 'question%d' % (question.id)
			if question_key not in request.POST:
				has_error = True
				error_msg = "Missing answer for question %d" % (question.sequence_num)
				break
			choices = [int(choice) for choice in request.POST.getlist(question_key)]
			if question.select_multiple and len(choices) > 10:
				has_error = True
				error_msg = "You selected too many choices for question %d, maximum number of choices is 10" % (question.sequence_num)
				break
			request.session[str(question.id)] = choices
		if has_error:
			return render(request, 'censustest/topic.html', {
				'topic': topic,
				'error_message': error_msg
			})

	if int(sequence_num) < num_topics:
		return HttpResponseRedirect(reverse('censustest:topic', args=(int(sequence_num) + 1,)))
	else:
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
				if str(question.id) not in self.request.session:
					context['error_message'] = 'Missing choices for some questions. Please do test again.'
					context['charts'] = []
					context['chart_div_ids'] = ''
					return context
				else:
					choices = self.request.session[str(question.id)]
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
