from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
	path('', views.IndexView.as_view(), name='index'),
	path('tl/', views.test_require_login, name='tl'),
	path('login/', views.LoginView.as_view(), name='login'),
	path('register/', views.RegisterView.as_view(), name='register'),
]