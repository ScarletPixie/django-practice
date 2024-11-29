from django.db import models

# Create your models here.
class Question(models.Model):
	question = models.CharField(max_length=100, unique=True, null=False)
	pub = models.DateTimeField("published date", null=False)

	def __str__(self):
		return self.question

class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice = models.CharField(max_length=100, null=False, unique=True)
	votes = models.IntegerField(default=0)

	def __str__(self):
		return self.choice