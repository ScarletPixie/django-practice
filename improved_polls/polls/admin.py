from django.contrib import admin
from .models import Question, Alternative

class AlternativeInline(admin.TabularInline):
	extra = 4
	model = Alternative
	readonly_fields = ['pk']
	verbose_name = 'alternatives'

class QuestionAdmin(admin.ModelAdmin):
	inlines = [AlternativeInline]
	fieldsets = [
		('Question', {'fields': ['text', 'pk']}),
		('Date Information', {'fields': ['pub_date']}),
	]
	list_display = ['text', 'pub_date', 'was_published_recently']
	readonly_fields = ['pk']
	search_fields = ['text', 'pub_date']

# Register your models here.
admin.site.register(Question, QuestionAdmin)
admin.site.register(Alternative)
