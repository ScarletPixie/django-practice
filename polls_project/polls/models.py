from django.db import models
import datetime
from django.utils import timezone

# Create your models here.
class Question(models.Model):
	question = models.CharField(max_length=100, unique=True, null=False)
	pub = models.DateTimeField("published date", null=False)

	def __str__(self):
		return self.question

	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.pub <= now


class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice = models.CharField(max_length=100, null=False)
	votes = models.IntegerField(default=0)

	def __str__(self):
		return self.choice

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=['question', 'choice'], name='unique_choice_per_question'),
		]
