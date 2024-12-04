from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
class Question(models.Model):
	text = models.CharField(max_length=100, verbose_name='question text', unique=True)
	pub_date = models.DateTimeField(default=timezone.now, verbose_name='publication date')

	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.pub_date <= now

	def __str__(self):
		return self.text

class Alternative(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='alternatives')
	text = models.CharField(max_length=100, verbose_name='alternative text')

	def __str__(self):
		return self.text

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=['question', 'text'], name='unique_alternative_per_question'),
		]