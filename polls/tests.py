import datetime

from django.core.urlresolvers import reverse
from django.utils import timezone
from django.test import TestCase

from polls.models import Poll

class PollMethodTests(TestCase):
    def test_was_published_recently_with_future_poll(self):
        ''' should return false when pub_date is in future'''
        future_poll = Poll(pub_date = timezone.now() + datetime.timedelta(days=30))
        self.assertEqual(future_poll.was_published_recently(), False)

    def test_was_published_recently_with_old_poll(self):
        ''' should return false when pub_date is in past 30 days'''
        old_poll = Poll(pub_date = timezone.now() - datetime.timedelta(days=30))
        self.assertEqual(old_poll.was_published_recently(), False)

    def test_was_published_recently_with_recent_poll(self):
        ''' should return false when pub_date is recent'''
        recent_poll = Poll(pub_date = timezone.now() - datetime.timedelta(hours=1))
        self.assertEqual(recent_poll.was_published_recently(), True)

def create_poll(question, days):
    '''create a poll with the given question, days delta'''
    return Poll.objects.create(question=question, pub_date=timezone.now() + datetime.timedelta(days=days))

class PollViewTests(TestCase):
    def test_index_view_with_no_polls(self):
        '''if no polls exist, display message'''
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertEqual(response.context['latest_poll_list'],[])

    def test_index_view_with_past_poll(self):
        '''should be displayed on the index page'''
        create_poll('past poll.', -30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_poll_list'], ['<Poll: past poll.>'])

    def test_index_view_with_future_poll(self):
        '''should not display future poll on index page'''
        create_poll('future poll', 30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are available.', status_code=200)
        self.assertQuerysetEqual(response.context['latest_poll_list'], [])

    def test_index_view_with_future_poll_and_past_poll(self):
        '''should only display past'''
        create_poll(question='past', days=-30)
        create_poll(question='future', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_poll_list'], ['<Poll: past>'])

    def test_index_view_with_two_past_polls(self):
        '''poll index may display multiple polls'''
        create_poll(question='past1', days=-30)
        create_poll(question='past2', days=-40)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_poll_list'],['<Poll: past1>','<Poll: past2>'])

class PollIndexDetailTests(TestCase):
    def test_detail_view_with_future_poll(self):
        '''detail view of future poll should return 404'''
        future_poll = create_poll(question='future', days=10)
        response = self.client.get(reverse('polls:detail', args=(future_poll.id,))) #TODO
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_past_poll(self):
        '''should display poll'''
        past_poll = create_poll(question='past', days=-10)
        response = self.client.get(reverse('polls:detail', args=(past_poll.id,)))
        self.assertContains(response, past_poll.question, status_code=200)
