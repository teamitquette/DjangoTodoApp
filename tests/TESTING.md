# Testing Guide for Todo Django Project

This document provides comprehensive information about running tests for the Todo Django project.

## Overview

The project includes comprehensive unit tests covering:
- **Models**: TodoItem model functionality, validation, and edge cases
- **Forms**: TodoItemForm validation, widgets, and labels
- **Views**: All CRUD operations (Create, Read, Update, Delete)
- **Edge Cases**: Boundary conditions, special characters, performance
- **Performance**: Large dataset handling and query optimization

## Test Structure

```
todoproject/
├── todo/
│   ├── tests.py              # Main test file with all test cases
│   ├── test_config.py        # Test configuration and utilities
│   └── ...
├── run_tests.py              # Test runner script
├── requirements-test.txt     # Test dependencies
└── TESTING.md               # This file
```

## Test Classes

### 1. TodoItemModelTest
Tests the TodoItem model functionality:
- Object creation and validation
- String representation
- Default values
- Ordering (by created_at)
- Field updates and completion status

### 2. TodoItemFormTest
Tests the TodoItemForm:
- Valid data submission
- Invalid data validation
- Field constraints (max length, required fields)
- Widget attributes and labels

### 3. TodoViewsTest
Tests all class-based views:
- TodoListView (list display)
- AddTodoView (create)
- EditTodoView (update)
- DeleteTodoView (delete)
- GET and POST requests
- Success/error handling
- Template usage

### 4. TodoItemEdgeCasesTest
Tests boundary conditions:
- Maximum field lengths
- Special characters and Unicode
- Whitespace handling
- Bulk operations

### 5. TodoItemPerformanceTest
Tests performance aspects:
- Large dataset creation (1000+ items)
- Query performance
- Filtering efficiency

## Running Tests

### Prerequisites

1. **Install test dependencies:**
   ```bash
   pip install -r requirements-test.txt
   ```

2. **Ensure Django is properly configured:**
   ```bash
   python manage.py check
   ```

### Basic Test Execution

#### Option 1: Using Django's manage.py
```bash
# Run all tests
python manage.py test

# Run with verbose output
python manage.py test --verbosity=2

# Run specific test class
python manage.py test todo.tests.TodoItemModelTest

# Run specific test method
python manage.py test todo.tests.TodoItemModelTest.test_todo_item_creation

# Run tests in parallel (faster)
python manage.py test --parallel
```

#### Option 2: Using the test runner script
```bash
# Run all tests
python run_tests.py

# Run with specific Django test arguments
python run_tests.py test --verbosity=2 --parallel
```

#### Option 3: Using pytest (if installed)
```bash
# Install pytest-django
pip install pytest-django

# Run tests
pytest

# Run with coverage
pytest --cov=todo --cov-report=html
```

### Test Coverage

To run tests with coverage reporting:

```bash
# Install coverage
pip install coverage

# Run tests with coverage
coverage run --source='.' manage.py test

# Generate coverage report
coverage report

# Generate HTML coverage report
coverage html
```

## Test Configuration

The `test_config.py` file provides:
- `TodoTestCase`: Base test class with common setup
- `TodoTestData`: Constants for test data
- Helper functions for common assertions

## Writing New Tests

### Adding Model Tests
```python
def test_new_model_feature(self):
    """Test description of what is being tested."""
    # Arrange
    todo = self.create_todo_item(title="Test")
    
    # Act
    result = todo.new_feature()
    
    # Assert
    self.assertEqual(result, expected_value)
```

### Adding View Tests
```python
def test_new_view_feature(self):
    """Test new view functionality."""
    # Arrange
    data = {'field': 'value'}
    
    # Act
    response = self.client.post(reverse('view_name'), data)
    
    # Assert
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'expected_content')
```

## Test Best Practices

1. **Test Naming**: Use descriptive test method names
2. **Documentation**: Include docstrings explaining test purpose
3. **Setup**: Use setUp() for common test data
4. **Cleanup**: Tests should clean up after themselves
5. **Isolation**: Each test should be independent
6. **Assertions**: Use specific assertions (assertEqual vs assertTrue)

## Common Test Patterns

### Testing Model Validation
```python
def test_model_validation(self):
    with self.assertRaises(ValidationError):
        TodoItem.objects.create(title='')  # Invalid data
```

### Testing Form Validation
```python
def test_form_validation(self):
    form = TodoItemForm(data={'title': ''})
    self.assertFalse(form.is_valid())
    self.assertIn('title', form.errors)
```

### Testing View Responses
```python
def test_view_response(self):
    response = self.client.get(reverse('view_name'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'template.html')
```

### Testing Database Operations
```python
def test_database_operation(self):
    initial_count = TodoItem.objects.count()
    TodoItem.objects.create(title='New Todo')
    self.assertEqual(TodoItem.objects.count(), initial_count + 1)
```

## Troubleshooting

### Common Issues

1. **Database errors**: Ensure test database is properly configured
2. **Import errors**: Check Python path and Django setup
3. **Template errors**: Verify template files exist and are accessible
4. **URL errors**: Ensure URL patterns are correctly defined

### Debugging Tests

```bash
# Run tests with debug output
python manage.py test --verbosity=3

# Run single test with debugger
python manage.py test todo.tests.TodoItemModelTest.test_todo_item_creation --debug-mode
```

## Performance Considerations

- Tests should complete quickly (under 1 second for most tests)
- Use `@skip` decorator for slow tests during development
- Consider using `@override_settings` for database optimization
- Use `bulk_create` for large dataset tests

## Continuous Integration

For CI/CD pipelines, consider:
- Running tests on multiple Python versions
- Testing against different databases
- Code coverage thresholds
- Performance benchmarks

## Additional Resources

- [Django Testing Documentation](https://docs.djangoproject.com/en/stable/topics/testing/)
- [Python unittest Documentation](https://docs.python.org/3/library/unittest.html)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [pytest-django Documentation](https://pytest-django.readthedocs.io/)
