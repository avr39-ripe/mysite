from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils import timezone
#import sys

import datetime
from polls.models import Poll

# Create your tests here.

class PollMethodTest(TestCase):
    def test_was_published_recently_with_future_poll(self):
        """
        was_published_recently() should return False of polls from future
        """
        future_poll = Poll(pub_date=timezone.now() + datetime.timedelta(days=30))
        self.assertEqual(future_poll.was_published_recently(), False)

    def test_was_published_recently_with_old_poll(self):
        """
        was_published_recently() should return False for old polls
        """
        old_poll = Poll(pub_date=timezone.now() - datetime.timedelta(days=30))
        self.assertEqual(old_poll.was_published_recently(), False)

    def test_was_published_recently_with_recent_poll(self):
        """
        was_published_recently() should return True for recent polls
        """
        recent_poll = Poll(pub_date=timezone.now() - datetime.timedelta(hours=1))
        self.assertEqual(recent_poll.was_published_recently(), True)

def create_poll(question, days):
    return Poll.objects.create(question=question, pub_date=timezone.now()+datetime.timedelta(days=days))

class PollViewTests(TestCase):
    def test_index_view_with_no_polls(self):
        """
        If no polls exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('polls:index'))
#        print >> sys.stderr, response
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls available")
        self.assertQuerysetEqual(response.context['latest_poll_list'], [])

    def test_index_view_with_past_poll(self):
        create_poll(question="Past poll.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_poll_list'],['<Poll: Past poll.>'])

    def test_index_view_with_future_polls(self):
        create_poll(question="Future poll.", days=30)
        response = self.client.get(reverse('polls:index'))
#        print >> sys.stderr, response
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls available")
        self.assertQuerysetEqual(response.context['latest_poll_list'], [])

    def test_index_view_with_past_and_future_polls(self):
        create_poll(question="Past poll.", days=-30)
        create_poll(question="Future poll", days=30)
        response = self.client.get(reverse('polls:index'))
#        print >> sys.stderr, response
        self.assertQuerysetEqual(response.context['latest_poll_list'],['<Poll: Past poll.>'])

class PollIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_poll(self):
        """
        The detail view of a poll with a pub_date in the future should
        return a 404 not found.
        """
        future_poll = create_poll(question='Future poll.', days=5)
        response = self.client.get(reverse('polls:detail', args=(future_poll.id,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_poll(self):
        """
        The detail view of a poll with a pub_date in the past should display
        the poll's question.
        """
        past_poll = create_poll(question='Past Poll.', days=-5)
        response = self.client.get(reverse('polls:detail', args=(past_poll.id,)))
        self.assertContains(response, past_poll.question, status_code=200)

