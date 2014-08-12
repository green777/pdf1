import datetime
from django.utils import timezone
from django.db import models

class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published') #human readable name. 1st pos
    def __unicode__(self):
        return self.question

    def was_published_recently(self):
        return timezone.now() >= self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'pubed recently?' #what for??


class Choice(models.Model):
    poll = models.ForeignKey(Poll) #each choice related to a single Poll
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __unicode__(self):
        return self.choice_text
