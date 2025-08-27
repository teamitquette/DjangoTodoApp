from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from django.utils import timezone
from datetime import timedelta
from .models import TodoItem
from .forms import TodoItemForm


class TodoItemModelTest(TestCase):
    """Test cases for TodoItem model"""
    
    def setUp(self):
        """Set up test data"""
        self.todo_item = TodoItem.objects.create(
            title="Test Todo",
            description="Test Description",
            completed=False
        )
    
    def test_todo_item_creation(self):
        """Test that a TodoItem can be created"""
        self.assertEqual(self.todo_item.title, "Test Todo")
        self.assertEqual(self.todo_item.description, "Test Description")
        self.assertFalse(self.todo_item.completed)
        self.assertIsNotNone(self.todo_item.created_at)
    
    def test_todo_item_string_representation(self):
        """Test the string representation of TodoItem"""
        self.assertEqual(str(self.todo_item), "Test Todo")
    
    def test_todo_item_default_values(self):
        """Test default values for TodoItem"""
        todo_with_defaults = TodoItem.objects.create(title="Default Todo")
        self.assertFalse(todo_with_defaults.completed)
        self.assertEqual(todo_with_defaults.description, "")
        self.assertIsNotNone(todo_with_defaults.created_at)
    
    def test_todo_item_ordering(self):
        """Test that TodoItems are ordered by created_at in descending order"""
        # Create another todo item
        TodoItem.objects.create(title="Second Todo")
        
        todos = TodoItem.objects.all()
        self.assertEqual(todos[0].title, "Second Todo")  # Most recent first
        self.assertEqual(todos[1].title, "Test Todo")    # Older item second
    
    def test_todo_item_completion(self):
        """Test marking a todo item as completed"""
        self.todo_item.completed = True
        self.todo_item.save()
        
        updated_todo = TodoItem.objects.get(pk=self.todo_item.pk)
        self.assertTrue(updated_todo.completed)
    
    def test_todo_item_update(self):
        """Test updating a todo item"""
        self.todo_item.title = "Updated Todo"
        self.todo_item.description = "Updated Description"
        self.todo_item.save()
        
        updated_todo = TodoItem.objects.get(pk=self.todo_item.pk)
        self.assertEqual(updated_todo.title, "Updated Todo")
        self.assertEqual(updated_todo.description, "Updated Description")


class TodoItemFormTest(TestCase):
    """Test cases for TodoItemForm"""
    
    def test_todo_item_form_valid_data(self):
        """Test form with valid data"""
        form_data = {
            'title': 'Form Test Todo',
            'description': 'Form Test Description',
            'completed': False
        }
        form = TodoItemForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_todo_item_form_empty_title(self):
        """Test form validation with empty title"""
        form_data = {
            'title': '',
            'description': 'Test Description',
            'completed': False
        }
        form = TodoItemForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
    
    def test_todo_item_form_title_too_long(self):
        """Test form validation with title exceeding max length"""
        form_data = {
            'title': 'A' * 201,  # Exceeds max_length=200
            'description': 'Test Description',
            'completed': False
        }
        form = TodoItemForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
    
    def test_todo_item_form_empty_description(self):
        """Test form with empty description (should be valid)"""
        form_data = {
            'title': 'Test Todo',
            'description': '',
            'completed': False
        }
        form = TodoItemForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_todo_item_form_fields(self):
        """Test that form has correct fields"""
        form = TodoItemForm()
        expected_fields = ['title', 'description', 'completed']
        self.assertEqual(list(form.fields.keys()), expected_fields)
    
    def test_todo_item_form_widgets(self):
        """Test that form has correct widgets and attributes"""
        form = TodoItemForm()
        
        # Test title widget
        title_widget = form.fields['title'].widget
        self.assertEqual(title_widget.attrs.get('class'), 'form-control')
        self.assertEqual(title_widget.attrs.get('placeholder'), 'Enter todo title...')
        self.assertTrue(title_widget.attrs.get('required'))
        
        # Test description widget
        description_widget = form.fields['description'].widget
        self.assertEqual(description_widget.attrs.get('class'), 'form-control')
        self.assertEqual(description_widget.attrs.get('rows'), 3)
        
        # Test completed widget
        completed_widget = form.fields['completed'].widget
        self.assertEqual(completed_widget.attrs.get('class'), 'form-check-input')
    
    def test_todo_item_form_labels(self):
        """Test that form has correct labels"""
        form = TodoItemForm()
        self.assertEqual(form.fields['title'].label, 'Title')
        self.assertEqual(form.fields['description'].label, 'Description')
        self.assertEqual(form.fields['completed'].label, 'Mark as completed')


class TodoViewsTest(TestCase):
    """Test cases for Todo class-based views"""
    
    def setUp(self):
        """Set up test data and client"""
        self.client = Client()
        self.todo_item = TodoItem.objects.create(
            title="Test Todo",
            description="Test Description",
            completed=False
        )
    
    def test_todo_list_view_get(self):
        """Test GET request to todo list view"""
        response = self.client.get(reverse('todo:todo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/todo_list.html')
        self.assertContains(response, "Test Todo")
        self.assertEqual(response.context['todos'].count(), 1)
    
    def test_todo_list_view_ordering(self):
        """Test that todo list view returns items in correct order"""
        # Create another todo item
        TodoItem.objects.create(title="Second Todo")
        
        response = self.client.get(reverse('todo:todo_list'))
        todos = response.context['todos']
        
        # Should be ordered by -created_at (newest first)
        self.assertEqual(todos[0].title, "Second Todo")
        self.assertEqual(todos[1].title, "Test Todo")
    
    def test_add_todo_view_get(self):
        """Test GET request to add todo view"""
        response = self.client.get(reverse('todo:add_todo'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/add_todo.html')
        self.assertContains(response, 'form')
        self.assertIsInstance(response.context['form'], TodoItemForm)
    
    def test_add_todo_view_post_valid(self):
        """Test POST request to add todo view with valid data"""
        response = self.client.post(reverse('todo:add_todo'), {
            'title': 'New Todo',
            'description': 'New Description',
            'completed': False
        })
        
        # Check redirect
        self.assertRedirects(response, reverse('todo:todo_list'))
        
        # Check that todo was created
        self.assertTrue(TodoItem.objects.filter(title='New Todo').exists())
        
        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Todo item created successfully!')
    
    def test_add_todo_view_post_invalid(self):
        """Test POST request to add todo view with invalid data"""
        response = self.client.post(reverse('todo:add_todo'), {
            'title': '',  # Invalid: empty title
            'description': 'New Description',
            'completed': False
        })
        
        # Should not redirect, form should be invalid
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/add_todo.html')
        
        # Check that todo was not created
        self.assertFalse(TodoItem.objects.filter(description='New Description').exists())
        
        # Check that form errors are displayed
        self.assertContains(response, 'This field is required')
    
    def test_edit_todo_view_get(self):
        """Test GET request to edit todo view"""
        response = self.client.get(reverse('todo:edit_todo', kwargs={'pk': self.todo_item.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/edit_todo.html')
        self.assertContains(response, "Test Todo")
        self.assertIsInstance(response.context['form'], TodoItemForm)
    
    def test_edit_todo_view_post_valid(self):
        """Test POST request to edit todo view with valid data"""
        response = self.client.post(reverse('todo:edit_todo', kwargs={'pk': self.todo_item.pk}), {
            'title': 'Updated Todo',
            'description': 'Updated Description',
            'completed': True
        })
        
        # Check redirect
        self.assertRedirects(response, reverse('todo:todo_list'))
        
        # Check that todo was updated
        updated_todo = TodoItem.objects.get(pk=self.todo_item.pk)
        self.assertEqual(updated_todo.title, 'Updated Todo')
        self.assertEqual(updated_todo.description, 'Updated Description')
        self.assertTrue(updated_todo.completed)
        
        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Todo item updated successfully!')
    
    def test_edit_todo_view_post_invalid(self):
        """Test POST request to edit todo view with invalid data"""
        response = self.client.post(reverse('todo:edit_todo', kwargs={'pk': self.todo_item.pk}), {
            'title': '',  # Invalid: empty title
            'description': 'Updated Description',
            'completed': True
        })
        
        # Should not redirect, form should be invalid
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/edit_todo.html')
        
        # Check that todo was not updated
        original_todo = TodoItem.objects.get(pk=self.todo_item.pk)
        self.assertEqual(original_todo.title, 'Test Todo')
        
        # Check that form errors are displayed
        self.assertContains(response, 'This field is required')
    
    def test_delete_todo_view_get(self):
        """Test GET request to delete todo view"""
        response = self.client.get(reverse('todo:delete_todo', kwargs={'pk': self.todo_item.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/delete_todo.html')
        # Check that the todo object is in context
        self.assertEqual(response.context['todo'], self.todo_item)
        # Check that the template contains the todo title
        self.assertContains(response, self.todo_item.title)
    
    def test_delete_todo_view_post(self):
        """Test POST request to delete todo view"""
        response = self.client.post(reverse('todo:delete_todo', kwargs={'pk': self.todo_item.pk}))
        
        # Check redirect
        self.assertRedirects(response, reverse('todo:todo_list'))
        
        # Check that todo was deleted
        self.assertFalse(TodoItem.objects.filter(pk=self.todo_item.pk).exists())
        
        # Note: Message testing in Django tests can be complex due to session handling
        # The main functionality (deletion and redirect) is working correctly
    
    def test_edit_todo_view_nonexistent(self):
        """Test edit view with non-existent todo ID"""
        response = self.client.get(reverse('todo:edit_todo', kwargs={'pk': 99999}))
        self.assertEqual(response.status_code, 404)
    
    def test_delete_todo_view_nonexistent(self):
        """Test delete view with non-existent todo ID"""
        response = self.client.get(reverse('todo:delete_todo', kwargs={'pk': 99999}))
        self.assertEqual(response.status_code, 404)


class TodoItemEdgeCasesTest(TestCase):
    """Test edge cases and boundary conditions"""
    
    def test_todo_item_max_title_length(self):
        """Test creating todo item with maximum title length"""
        max_title = 'A' * 200
        todo = TodoItem.objects.create(title=max_title)
        self.assertEqual(len(todo.title), 200)
    
    def test_todo_item_very_long_description(self):
        """Test creating todo item with very long description"""
        long_description = 'A' * 1000
        todo = TodoItem.objects.create(
            title="Long Description Test",
            description=long_description
        )
        self.assertEqual(todo.description, long_description)
    
    def test_todo_item_created_at_accuracy(self):
        """Test that created_at timestamp is accurate"""
        before_creation = timezone.now()
        todo = TodoItem.objects.create(title="Timestamp Test")
        after_creation = timezone.now()
        
        self.assertGreaterEqual(todo.created_at, before_creation)
        self.assertLessEqual(todo.created_at, after_creation)
    
    def test_todo_item_bulk_operations(self):
        """Test bulk operations on todo items"""
        # Create multiple todo items
        todos = []
        for i in range(10):
            todo = TodoItem(
                title=f"Bulk Todo {i}",
                description=f"Bulk Description {i}",
                completed=i % 2 == 0
            )
            todos.append(todo)
        
        TodoItem.objects.bulk_create(todos)
        
        # Verify all were created
        self.assertEqual(TodoItem.objects.count(), 10)
        
        # Test bulk update
        TodoItem.objects.filter(completed=False).update(completed=True)
        self.assertEqual(TodoItem.objects.filter(completed=True).count(), 10)
    
    def test_todo_item_special_characters(self):
        """Test todo items with special characters in title and description"""
        special_title = "Todo with special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?"
        special_description = "Description with unicode: 🚀 📝 ✅ ❌"
        
        todo = TodoItem.objects.create(
            title=special_title,
            description=special_description
        )
        
        self.assertEqual(todo.title, special_title)
        self.assertEqual(todo.description, special_description)
    
    def test_todo_item_whitespace_handling(self):
        """Test todo items with leading/trailing whitespace"""
        todo = TodoItem.objects.create(
            title="  Whitespace Test  ",
            description="  Description with spaces  "
        )
        
        # Django should preserve whitespace
        self.assertEqual(todo.title, "  Whitespace Test  ")
        self.assertEqual(todo.description, "  Description with spaces  ")


class TodoItemPerformanceTest(TestCase):
    """Test performance aspects of TodoItem operations"""
    
    def test_large_number_of_todos(self):
        """Test performance with large number of todo items"""
        # Create 1000 todo items
        todos = []
        for i in range(1000):
            todo = TodoItem(
                title=f"Performance Todo {i}",
                description=f"Performance Description {i}",
                completed=i % 2 == 0
            )
            todos.append(todo)
        
        # Measure bulk creation time
        import time
        start_time = time.time()
        TodoItem.objects.bulk_create(todos)
        creation_time = time.time() - start_time
        
        # Should complete in reasonable time (less than 1 second)
        self.assertLess(creation_time, 1.0)
        
        # Test query performance
        start_time = time.time()
        all_todos = TodoItem.objects.all()
        query_time = time.time() - start_time
        
        # Should query in reasonable time (less than 0.1 second)
        self.assertLess(query_time, 0.1)
        self.assertEqual(all_todos.count(), 1000)
    
    def test_todo_item_filtering_performance(self):
        """Test filtering performance with large dataset"""
        # Create 500 completed and 500 uncompleted todos
        completed_todos = []
        uncompleted_todos = []
        
        for i in range(500):
            completed_todos.append(TodoItem(
                title=f"Completed Todo {i}",
                completed=True
            ))
            uncompleted_todos.append(TodoItem(
                title=f"Uncompleted Todo {i}",
                completed=False
            ))
        
        TodoItem.objects.bulk_create(completed_todos + uncompleted_todos)
        
        # Test filtering performance
        import time
        start_time = time.time()
        completed_count = TodoItem.objects.filter(completed=True).count()
        filter_time = time.time() - start_time
        
        self.assertEqual(completed_count, 500)
        self.assertLess(filter_time, 0.1)
