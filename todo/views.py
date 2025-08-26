from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import TodoItem
from .forms import TodoItemForm

# Class-based views
class TodoListView(ListView):
    model = TodoItem
    template_name = 'todo/todo_list.html'
    context_object_name = 'todos'
    ordering = ['-created_at']

class AddTodoView(CreateView):
    model = TodoItem
    form_class = TodoItemForm
    template_name = 'todo/add_todo.html'
    success_url = reverse_lazy('todo:todo_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Todo item created successfully!')
        return super().form_valid(form)

class EditTodoView(UpdateView):
    model = TodoItem
    form_class = TodoItemForm
    template_name = 'todo/edit_todo.html'
    success_url = reverse_lazy('todo:todo_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Todo item updated successfully!')
        return super().form_valid(form)

class DeleteTodoView(DeleteView):
    model = TodoItem
    template_name = 'todo/delete_todo.html'
    success_url = reverse_lazy('todo:todo_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Todo item deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Alternative function-based views if you prefer:
def todo_list(request):
    todos = TodoItem.objects.all().order_by('-created_at')
    return render(request, 'todo/todo_list.html', {'todos': todos})

def add_todo(request):
    if request.method == 'POST':
        form = TodoItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Todo item created successfully!')
            return redirect('todo_list')
    else:
        form = TodoItemForm()
    return render(request, 'todo/add_todo.html', {'form': form})

def edit_todo(request, pk):
    todo = get_object_or_404(TodoItem, pk=pk)
    if request.method == 'POST':
        form = TodoItemForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Todo item updated successfully!')
            return redirect('todo_list')
    else:
        form = TodoItemForm(instance=todo)
    return render(request, 'todo/edit_todo.html', {'form': form, 'todo': todo})

def delete_todo(request, pk):
    todo = get_object_or_404(TodoItem, pk=pk)
    if request.method == 'POST':
        todo.delete()
        messages.success(request, 'Todo item deleted successfully!')
        return redirect('todo_list')
    return render(request, 'todo/delete_todo.html', {'todo': todo})
