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
		return self.pub >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice = models.CharField(max_length=100, null=False, unique=True)
	votes = models.IntegerField(default=0)

	def __str__(self):
		return self.choice
