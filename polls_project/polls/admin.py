from django.contrib import admin

# Register your models here.
from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4
    readonly_fields = ['pk']
    verbose_name = "alternative"

class QuestionAdmin(admin.ModelAdmin):

	inlines = [ChoiceInline]
	fieldsets = [
		("Question", {"fields": ['question', 'pk']}),
		("Date Information", {"fields": ['pub']}),
	]
	readonly_fields = ['pk']
	list_display = ['question', 'pub', 'was_published_recently']
	list_filter = ['question', 'pub']
	search_fields = ['question']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
