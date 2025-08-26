# Django Todo Application

A modern, responsive todo list application built with Django and Bootstrap. This project demonstrates a complete CRUD (Create, Read, Update, Delete) application with a clean, user-friendly interface.

## Features

- **Create Todos**: Add new todo items with title, description, and completion status
- **List Todos**: View all todos in a responsive card layout
- **Edit Todos**: Modify existing todo items
- **Delete Todos**: Remove todos with confirmation
- **Mark Complete**: Toggle completion status
- **Modern UI**: Beautiful Bootstrap 5 interface with responsive design
- **Mobile Friendly**: Works perfectly on all device sizes
- **Success Messages**: User feedback for all operations
- **Fast & Lightweight**: Built with Django's efficient architecture

## Live Demo

Visit the application at: `http://localhost:8000/` (after starting the development server)

## Technology Stack

- **Backend**: Django 5.2.5
- **Frontend**: Bootstrap 5.3.0 + Bootstrap Icons
- **Database**: SQLite (default), easily configurable for PostgreSQL/MySQL
- **Python**: 3.8+
- **Template Engine**: Django Templates
- **Forms**: Django ModelForms with Bootstrap styling

## Prerequisites

Before running this application, make sure you have:

- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

## Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd ToDoList/todoproject
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 6. Start Development Server

```bash
python manage.py runserver
```

### 7. Access the Application

Open your browser and navigate to: `http://localhost:8000/`

## Project Structure

```
todoproject/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .gitignore              # Git ignore rules
├── README.md               # This file
├── todoproject/            # Main project settings
│   ├── __init__.py
│   ├── settings.py         # Django settings
│   ├── urls.py            # Main URL configuration
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
└── todo/                   # Todo app
    ├── __init__.py
    ├── admin.py            # Admin interface configuration
    ├── apps.py             # App configuration
    ├── forms.py            # Todo form definitions
    ├── models.py           # Todo data models
    ├── urls.py             # App URL patterns
    ├── views.py            # View logic
    ├── tests.py            # Test cases
    └── templates/          # HTML templates
        └── todo/
            ├── base.html           # Base template
            ├── todo_list.html      # Todo list view
            ├── add_todo.html       # Add todo form
            ├── edit_todo.html      # Edit todo form
            └── delete_todo.html    # Delete confirmation
```

## Usage Guide

### Adding a Todo

1. Click the "Add Todo" button in the navigation or on the main page
2. Fill in the title (required) and description (optional)
3. Check the "Mark as completed" box if the todo is already done
4. Click "Create Todo"

### Editing a Todo

1. Click the "Edit" button on any todo card
2. Modify the title, description, or completion status
3. Click "Update Todo"

### Deleting a Todo

1. Click the "Delete" button on any todo card
2. Confirm the deletion on the confirmation page
3. Click "Yes, Delete It"

### Marking as Complete

1. Edit a todo item
2. Check the "Mark as completed" checkbox
3. Save the changes

## Configuration

### Environment Variables

Create a `.env` file in the project root for environment-specific settings:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
```

### Database Configuration

The default configuration uses SQLite. To use PostgreSQL or MySQL, update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Testing

Run the test suite:

```bash
python manage.py test
```

Or use pytest (if installed):

```bash
pytest
```

## Admin Interface

Access the Django admin interface at `http://localhost:8000/admin/` to:

- View and manage all todo items
- Filter todos by completion status and creation date
- Search todos by title and description
- Bulk edit operations

## Deployment

### Production Settings

1. Set `DEBUG = False` in `settings.py`
2. Configure a production database
3. Set up static file serving
4. Configure environment variables
5. Use a production WSGI server like Gunicorn

### Docker Deployment

This project includes a complete Docker setup with:

- Multi-stage Dockerfile for optimized production builds
- Docker Compose configuration with PostgreSQL, Redis, and Nginx
- Production-ready Nginx reverse proxy configuration
- Health checks and monitoring

To deploy with Docker:

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f web

# Stop services
docker-compose down
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Django](https://www.djangoproject.com/) - The web framework
- [Bootstrap](https://getbootstrap.com/) - CSS framework
- [Bootstrap Icons](https://icons.getbootstrap.com/) - Icon library

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/your-repo/issues) page
2. Create a new issue with detailed information
3. Contact the maintainers

## Version History

- **v1.0.0** - Initial release with basic CRUD functionality
- **v1.1.0** - Added Bootstrap styling and responsive design
- **v1.2.0** - Enhanced admin interface and form validation
- **v1.3.0** - Added Docker support and production deployment configuration

---

**Happy coding!**
