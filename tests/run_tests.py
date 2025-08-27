#!/usr/bin/env python
"""
Test runner script for the Todo Django project.
This script provides an easy way to run tests with different options.
"""

import os
import sys
import django
from django.core.management import execute_from_command_line


def run_tests():
    """Run the Django test suite."""
    # Add the project directory to Python path
    project_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_dir)
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todoproject.settings')
    django.setup()
    
    # Run tests with different options
    if len(sys.argv) > 1:
        # User provided specific test arguments
        execute_from_command_line(sys.argv)
    else:
        # Default test run
        print("Running all tests...")
        print("=" * 50)
        
        # Run tests with coverage if available
        try:
            import coverage
            print("Running tests with coverage...")
            execute_from_command_line(['manage.py', 'test', '--verbosity=2', '--parallel'])
        except ImportError:
            print("Coverage not available, running tests without coverage...")
            execute_from_command_line(['manage.py', 'test', '--verbosity=2', '--parallel'])
        
        print("=" * 50)
        print("Tests completed!")


if __name__ == '__main__':
    run_tests()
