from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.shortcuts import get_object_or_404
from .models import Question, Choice

# Create your views here.
class IndexView(generic.ListView):
	context_object_name = 'question_list'
	template_name = 'polls/index.html'

	def get_queryset(self):
		return Question.objects.order_by('-pub')[:5]

class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'

def results(request, pk):
	question = get_object_or_404(Question, pk=pk)
	return render(request, 'polls/results.html', {'question':question})

def vote(request, pk):
	question = get_object_or_404(Question, pk=pk)
	
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.html', {'question': question, 'error_message':"you didn't select a choice"})
	selected_choice.votes = F('votes') + 1
	selected_choice.save()

	return HttpResponseRedirect(reverse('polls:results', kwargs={'pk':question.pk}))