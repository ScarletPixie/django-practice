from django.urls import path
from . import views

app_name='docs_app'
urlpatterns = [
    path('create/', views.create, name='create'),
    path('dog/<int:pk>/', views.detail, name='detail'),
]
