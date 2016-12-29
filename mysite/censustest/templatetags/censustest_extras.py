from django import template

register = template.Library()

@register.filter
def get_stats(question, stats_dict):
	return stats_dict[question.id]

@register.filter
def sort_choices(question):
	if question.alphabetical_choices:
		return question.choice_set.order_by('text')
	else:
		return question.choice_set.order_by('id')
