"""
Test configuration and utilities for Todo app tests.
This file provides common test setup and helper functions.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from .models import TodoItem


class TodoTestCase(TestCase):
    """Base test case class with common setup for Todo app tests."""
    
    def setUp(self):
        """Set up common test data."""
        super().setUp()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def create_todo_item(self, title="Test Todo", description="Test Description", completed=False):
        """Helper method to create a TodoItem for testing."""
        return TodoItem.objects.create(
            title=title,
            description=description,
            completed=completed
        )
    
    def create_multiple_todos(self, count=5):
        """Helper method to create multiple TodoItems for testing."""
        todos = []
        for i in range(count):
            todo = self.create_todo_item(
                title=f"Todo {i}",
                description=f"Description {i}",
                completed=i % 2 == 0
            )
            todos.append(todo)
        return todos


class TodoTestData:
    """Class containing test data constants."""
    
    VALID_TODO_DATA = {
        'title': 'Valid Todo Title',
        'description': 'Valid todo description',
        'completed': False
    }
    
    INVALID_TODO_DATA = {
        'title': '',  # Empty title is invalid
        'description': 'Invalid todo description',
        'completed': False
    }
    
    LONG_TITLE_DATA = {
        'title': 'A' * 201,  # Exceeds max_length=200
        'description': 'Todo with long title',
        'completed': False
    }
    
    SPECIAL_CHARS_DATA = {
        'title': 'Todo with special chars: !@#$%^&*()_+-=[]{}|;\':",./<>?',
        'description': 'Description with unicode: 🚀 📝 ✅ ❌',
        'completed': True
    }
    
    WHITESPACE_DATA = {
        'title': '  Todo with whitespace  ',
        'description': '  Description with spaces  ',
        'completed': False
    }


def assert_todo_item_attributes(test_case, todo, expected_title, expected_description, expected_completed):
    """Helper function to assert TodoItem attributes."""
    test_case.assertEqual(todo.title, expected_title)
    test_case.assertEqual(todo.description, expected_description)
    test_case.assertEqual(todo.completed, expected_completed)
    test_case.assertIsNotNone(todo.created_at)


def assert_form_errors(test_case, form, expected_errors):
    """Helper function to assert form validation errors."""
    test_case.assertFalse(form.is_valid())
    for field, error_message in expected_errors.items():
        test_case.assertIn(field, form.errors)
        if error_message:
            test_case.assertIn(error_message, str(form.errors[field]))


def assert_success_message(test_case, response, expected_message):
    """Helper function to assert success messages in response."""
    messages = list(get_messages(response.wsgi_request))
    test_case.assertEqual(len(messages), 1)
    test_case.assertEqual(str(messages[0]), expected_message)
