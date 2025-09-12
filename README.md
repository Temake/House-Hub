# HouseHub- House Management API

A collaborative house management system built with Django REST Framework that allows users to create houses, join them, and manage household tasks together.

## Features

- User authentication with OAuth 2.0
- House creation and management
- Task management within houses
- Automatic points system
- Member management
- Google Cloud Storage integration for media files
- Background job processing

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)
- Google Cloud Storage account (for media storage)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/homesync.git
cd homesync
```

2. Create and activate a virtual environment:
```bash
python -m venv virtual_env
# On Windows
virtual_env\Scripts\activate
# On Unix or MacOS
source virtual_env/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```
DEBUG=True
SECRET_KEY=your-secret-key
GOOGLE_CLOUD_STORAGE_BUCKET=your-bucket-name
GOOGLE_CLOUD_CREDENTIALS=path-to-your-credentials.json
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register a new user
- `POST /api/auth/login/` - Login user
- `POST /api/auth/logout/` - Logout user

### Houses
- `GET /api/house/` - List all houses
- `POST /api/house/` - Create a new house
- `GET /api/house/{id}/` - Get house details
- `PUT /api/house/{id}/` - Update house details
- `DELETE /api/house/{id}/` - Delete a house

#### House Actions
- `POST /api/house/{id}/join/` - Join a house
- `POST /api/house/{id}/leave/` - Leave a house
- `POST /api/house/{id}/remove_member/` - Remove a member from house (Manager only)

### Tasks
- `GET /api/tasks/` - List all tasks
- `POST /api/tasks/` - Create a new task
- `GET /api/tasks/{id}/` - Get task details
- `PUT /api/tasks/{id}/` - Update task
- `DELETE /api/tasks/{id}/` - Delete task

## Project Structure

```
homesync/
├── backgroundjobs/    # Background task processing
├── house/            # Main house management app
├── task/             # Task management app
├── users/            # User management app
├── main/             # Project configuration
├── media/            # Media files storage
└── manage.py         # Django management script
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Django REST Framework
- Google Cloud Storage
- All contributors who have helped shape this project

