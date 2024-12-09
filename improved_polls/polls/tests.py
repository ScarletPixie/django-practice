from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Question
import datetime

def create_question(text, days):
	return Question.objects.create(text=text, pub_date=timezone.now() + datetime.timedelta(days=days))

# Create your tests here.
class IndexViewTests(TestCase):
	def test_index_displays_questions(self):
		questions = []
		for i in range(5):
			questions.append(create_question(f'Who are you {i}', -i))
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		for i in range(5):
			self.assertContains(response, f'Who are you {i}')
		