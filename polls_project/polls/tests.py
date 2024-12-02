from django.test import TestCase
from .models import Question
from django.utils import timezone
from django.test.utils import setup_test_environment, teardown_test_environment
from django.urls import reverse
import datetime

# Question specific tests
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
        one_day_old_question = Question(pub = time1)
        very_old_question = Question(pub = time2)
        self.assertIs(one_day_old_question.was_published_recently(), False)
        self.assertIs(very_old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently returns True for questions published within a day
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=50)
        recent1 = Question(pub = time)
        recent2 = Question(pub = timezone.now())
        self.assertIs(recent1.was_published_recently(), True)
        self.assertIs(recent2.was_published_recently(), True)

# view specific tests
#  helper function
def create_question(text: str, days: int):
    """ cretes a new Question object with parameters text and days offset from timezone.now() """
    return Question.objects.create(pub=timezone.now() + datetime.timedelta(days=days), question=text)

class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """
        shows 'no polls available' if there are no questions or no questions with a past date
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls available')
        self.assertQuerySetEqual(response.context['question_list'], [])

    def test_past_questions(self):
        question = create_question(text='dummy question 0', days=-10)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'dummy question 0')
        self.assertQuerySetEqual(response.context['question_list'], [question])


    def test_only_shows_5_recent_questions(self):
        """
        Only the 5 most recent questions excluding future questions are sent to index
        """
        question_num = 10
        questions = []
        for i in range(question_num):
            questions.append(create_question(text=f"dummy question {i}", days=-i))

        _ = create_question(text="back to the future", days=1000)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)

        for i in range(question_num):
            if (i < 5):
                self.assertContains(response, f"dummy question {i}")
            else:
                self.assertNotContains(response, f"dummy question {i}")

        self.assertQuerySetEqual(response.context['question_list'], questions[:5])
