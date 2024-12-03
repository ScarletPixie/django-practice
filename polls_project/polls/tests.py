from django.test import TestCase
from .models import Question, Choice
from django.utils import timezone
from django.test.utils import setup_test_environment, teardown_test_environment
from django.urls import reverse
import datetime
import html

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


class QuestionDetailViewTests(TestCase):
    def test_with_no_valid_question(self):
        future_question = create_question('dummy question', 10)
        response = self.client.get(reverse('polls:detail', kwargs={'pk':future_question.pk}))
        self.assertEqual(response.status_code, 404)

    def test_with_valid_question(self):
        question = create_question('dummy question', -10)
        response = self.client.get(reverse('polls:detail', kwargs={'pk':question.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'dummy question')
        self.assertEqual(response.context['question'], question)
    
    def test_with_invalid_question_id(self):
        response = self.client.get(reverse('polls:detail', kwargs={'pk':10000000000}))
        self.assertEqual(response.status_code, 404)


class QuestionResultsViewTests(TestCase):
    future = 10
    past = -10
    dummy_text = 'dummy question'
    def get_url(self, pk: int):
        return reverse('polls:results', kwargs={'pk':pk})

    def test_with_no_questions(self):
        """
        Should return 404 on any id given with no questions
        """
        response = self.client.get(self.get_url(0))
        self.assertEqual(response.status_code, 404)

    def test_with_valid_question(self):
        """
        Should return 200 and display the question
        """
        question = create_question(self.dummy_text, self.past)
        response = self.client.get(self.get_url(question.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.dummy_text)
        self.assertEqual(response.context['question'], question)

    def test_with_future_question(self):
        """
        Should return 404 on a future question
        """
        question = create_question(self.dummy_text, self.future)
        response = self.client.get(self.get_url(question.pk))
        self.assertEqual(response.status_code, 404)


class VoteViewTests(TestCase):
    future = 10
    past = -10
    dummy_text = 'dummy question'
    def get_url(self, pk: int):
        return reverse('polls:vote', kwargs={'pk':pk})

    def test_future_question_returns_404(self):
        """
        trying to vote on a future question should return 404 and not update the votes count for that question
        """
        question = create_question(self.dummy_text, self.future)
        choice = Choice.objects.create(question=question, choice=self.dummy_text)
        response = self.client.post(self.get_url(question.pk), data={'choice':choice.pk}, follow=True)
        choice.refresh_from_db()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(choice.votes, 0)

    def test_no_post_data_returns_error(self):
        """
        trying to post data to vote without sending 'choice' should be redirected to detail page with an error
        """
        question = create_question(self.dummy_text, self.past)
        choice = Choice.objects.create(question=question, choice=self.dummy_text)
        response = self.client.post(self.get_url(question.pk), data={})
        choice.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(choice.votes, 0)
        self.assertEqual(response.context['error_message'], "you didn't select a choice")
        self.assertEqual(response.context['question'], question)
        self.assertIn("you didn't select a choice", html.unescape(response.content.decode()))

    def test_increases_vote_count_with_valid_request(self):
        """
        should increase vote count on a valid request
        """
        question = create_question(self.dummy_text, self.past)
        choice = Choice.objects.create(question=question, choice=self.dummy_text)
        response = self.client.post(self.get_url(question.pk), data={'choice':choice.pk})
        choice.refresh_from_db()
        self.assertEqual(choice.votes, 1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('polls:results', kwargs={'pk':question.pk}))
    
    def test_with_mismatched_choice_question_id(self):
        """
        should not alter database in case of invalid request
        """
        question1 = create_question(self.dummy_text, self.past)
        question2 = create_question(f"{self.dummy_text}2", self.past)
        choice1 = Choice.objects.create(question=question1, choice=self.dummy_text)
        choice2 = Choice.objects.create(question=question2, choice=self.dummy_text)
        response1 = self.client.post(self.get_url(question1.pk), data={'choice':choice2.pk})
        response2 = self.client.post(self.get_url(question2.pk), data={'choice':choice1.pk})
        choice1.refresh_from_db()
        choice2.refresh_from_db()
        self.assertEqual(choice1.votes, 0)
        self.assertEqual(choice2.votes, 0)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response1.context['error_message'], "you didn't select a choice")
        self.assertEqual(response2.context['error_message'], "you didn't select a choice")
        self.assertEqual(response1.context['question'], question1)
        self.assertEqual(response2.context['question'], question2)
        self.assertIn("you didn't select a choice", html.unescape(response1.content.decode()))
        self.assertIn("you didn't select a choice", html.unescape(response2.content.decode()))
    
    def test_with_invalid_question_id(self):
        """
        should return 404 on missing/invalid question id
        """
        response = self.client.post(self.get_url(0), data={'pk':1})
        self.assertEqual(response.status_code, 404)