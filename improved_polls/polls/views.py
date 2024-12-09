from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Question

# Create your views here.

@login_required(login_url=reverse_lazy('polls:login'))
def test_require_login(request):
	return render(request, 'polls/index.html')


class IndexView(generic.ListView):
	model = Question
	template_name = 'polls/index.html'
	context_object_name = 'questions'

	def get_queryset(self):
		return Question.objects.order_by('-pub_date')[:5]

class RegisterView(generic.FormView):
	form_class = UserCreationForm
	template_name = 'polls/register.html'
	success_url = reverse_lazy('polls:index')

	def form_valid(self, form):
		user = form.save()
		login(self.request, user)
		return super().form_valid(form)

class LoginView(generic.FormView):
	form_class = AuthenticationForm
	template_name = 'polls/login.html'
	success_url = reverse_lazy('polls:index')

	def form_valid(self, form):
		authenticate(self.request.user)
		login(self.request, self.request.user)
		return super().form_valid(form)