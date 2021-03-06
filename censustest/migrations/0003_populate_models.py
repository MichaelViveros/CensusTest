# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-22 13:27
from __future__ import unicode_literals

from django.db import migrations, models
from django.db.models import Sum

COL_TITLE = 0
COL_CHOICE = 1
COL_TOTAL = 2
COL_SOURCE = 3
COL_QUESTION = 4
COL_TOPIC = 5
COL_SEQUENCE_NUM = 6
COL_SELECT_MULTIPLE = 7

def populate_models(apps, schema_editor):
	Question = apps.get_model("censustest", "Question")
	Choice = apps.get_model("censustest", "Choice")

	f = open('censustest/migrations/0003_census_data.csv', 'r')

	# first row is header
	f.readline()

	prevNumLeadingSpaces = 0
	q = None
	c = None
	questions = []
	for line in f:
		cols = line.split(",")
		if cols[COL_QUESTION] != "":
			q = Question.objects.create(
				text=cols[COL_QUESTION].strip(),
				title=cols[COL_TITLE],
				total_response_count=0,
				topic=cols[COL_TOPIC],
				sequence_num=cols[COL_SEQUENCE_NUM]
			)
			if cols[COL_SELECT_MULTIPLE] != "\n":
				q.select_multiple=bool(cols[COL_SELECT_MULTIPLE])
			questions.append(q)
		else:
			choice = cols[COL_CHOICE]

			numLeadingSpaces = len(choice) - len(choice.lstrip(" "))
			if numLeadingSpaces > 2 and numLeadingSpaces > prevNumLeadingSpaces:
				# remove previous choice since always want most specific choice (has most leading spaces)
				q.choice_set.last().delete()

			q.choice_set.create(
				text=cols[COL_CHOICE].strip(),
				response_count=int(cols[COL_TOTAL]),
				response_percent=0.0
			)

			prevNumLeadingSpaces = numLeadingSpaces

	for q in questions:
		choiceCounts = q.choice_set.aggregate(Sum('response_count'))['response_count__sum']
		q.total_response_count = choiceCounts
		q.save()
		for c in q.choice_set.all():
			c.response_percent = float(c.response_count) / choiceCounts
			c.save()

class Migration(migrations.Migration):

	dependencies = [
		('censustest', '0002_add_choice'),
	]

	operations = [
		migrations.RunPython(populate_models),
	]
