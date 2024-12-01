from django.test import TestCase
from .models import Question, Choice
from django.utils import timezone
import datetime

# Create your tests here.
class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently returns False for questions posted on th future
        """
        time = timezone.now() + datetime.timedelta(days = 30)
        future_question = Question(pub = time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently returns False for questions older than a 1 day
        """
        time1 = timezone.now() - datetime.timedelta(days = 1)
        time2 = timezone.now() - datetime.timedelta(days = 100)
        one_day_old_question = Question(pub = time1);
        very_old_question = Question(pub = time2);
        self.assertIs(one_day_old_question.was_published_recently(), False)
        self.assertIs(very_old_question.was_published_recently(), False)

