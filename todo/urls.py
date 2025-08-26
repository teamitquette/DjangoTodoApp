from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    # Class-based views
    path('', views.TodoListView.as_view(), name='todo_list'),
    path('add/', views.AddTodoView.as_view(), name='add_todo'),
    path('edit/<int:pk>/', views.EditTodoView.as_view(), name='edit_todo'),
    path('delete/<int:pk>/', views.DeleteTodoView.as_view(), name='delete_todo'),
]
