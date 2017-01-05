from django.db import models


class Topic(models.Model):
	text = models.CharField(max_length=200)
	sequence_num = models.IntegerField(unique=True)

	class Meta:
		ordering = ["sequence_num"]

	def __str__(self):
		return self.text

	def get_progress_percent(self):
		return int(100 * (self.sequence_num - 1) / Topic.objects.count())


class Question(models.Model):
	text = models.CharField(max_length=200)
	title = models.CharField(max_length=200)
	total_response_count = models.IntegerField()
	topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
	sequence_num = models.IntegerField()
	select_multiple = models.BooleanField(default=False)
	alphabetical_choices = models.BooleanField(default=True)
	description = models.CharField(max_length=1000, default='')
	footnote = models.CharField(max_length=1000, default='')

	class Meta:
		ordering = ["sequence_num"]

	def __str__(self):
		return self.text

	def _get_display_text(self):
		"Returns the display text of a question."
		return '%d. %s' % (self.sequence_num, self.text.replace(';', ','))
	display_text = property(_get_display_text)

	def get_stats(self, choice_ids):
		if len(choice_ids) == 0:
			return ['*You did not select a choice for this question']

		stats = []
		for choice_id in choice_ids:
			choice = self.choice_set.get(id=choice_id)
			stat_text = '%.1f%% of Canadians also selected %s' % (choice.response_percent, choice.text)
			stats.append(stat_text)

		return stats

	def get_chart_data(self, choice_ids):
		if len(choice_ids) > 10:
			return None

		num_choices_left = 10 - len(choice_ids)
		other_choice_ids = list(self.choice_set.exclude(id__in=choice_ids).values_list('id', flat=True).order_by('-response_percent')[:num_choices_left])

		chart_choice_ids = choice_ids + other_choice_ids
		chart_data = self.choice_set.filter(id__in=chart_choice_ids)
		return chart_data

class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	text = models.CharField(max_length=200)
	response_count = models.IntegerField()
	response_percent = models.FloatField()

	def _get_display_text(self):
		"Returns the display text of a choice."
		return self.text.replace(';', ',')
	display_text = property(_get_display_text)

	def __str__(self):
		return self.text
