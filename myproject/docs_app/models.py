from django.db import models

class Doc(models.Model):
    title = models.Charfield(max_length=50)
    text = models.textField(
