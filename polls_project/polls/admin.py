from django.contrib import admin

# Register your models here.
from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
	readonly_fields = ['pk']
	inlines = [ChoiceInline]

class ChoiceAdmin(admin.ModelAdmin):
	readonly_fields = ['pk']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
