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
    return Poll.objects.create(question=question, pub_date=timezone.now()+datetime.timedelta(deys=days))

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
