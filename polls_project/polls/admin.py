from django.contrib import admin

# Register your models here.
from .models import Question, Choice


class QuestionAdmin(admin.ModelAdmin):
	readonly_fields = ['pk']
class ChoiceAdmin(admin.ModelAdmin):
	readonly_fields = ['pk']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)