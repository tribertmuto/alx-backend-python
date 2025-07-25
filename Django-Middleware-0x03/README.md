# Django Middleware 0x03

A Django project demonstrating custom middleware implementation for request logging, access control, rate limiting, and role-based permissions.

## Features

### Custom Middleware

1. **RequestLoggingMiddleware**
   - Logs all incoming requests with user information and path
   - Stores logs in `requests.log` file

2. **RestrictAccessByTimeMiddleware**
   - Restricts access to chat functionality between 6PM and 9PM
   - Returns 403 Forbidden outside allowed hours

3. **OffensiveLanguageMiddleware**
   - Implements rate limiting for POST requests to `/chats/`
   - Limits to 5 messages per minute per IP address

4. **RolepermissionMiddleware**
   - Protects specific paths (`/chats/delete/`, `/chats/manage/`)
   - Requires admin or moderator role for access

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py migrate
```

3. Start the development server:
```bash
python manage.py runserver
```

## Usage

### Testing Middleware

1. **Basic Chat View**: Visit `http://localhost:8000/chats/`
2. **Send Message**: POST to `http://localhost:8000/chats/send/` with JSON body:
   ```json
   {
     "message": "Hello, world!"
   }
   ```

### Middleware Testing

- **Time Restriction**: Try accessing chat outside 6PM-9PM hours
- **Rate Limiting**: Send multiple POST requests quickly to `/chats/send/`
- **Role Protection**: Access protected paths without proper permissions
- **Request Logging**: Check `requests.log` for request details

## Project Structure

```
Django-Middleware-0x03/
├── manage.py
├── settings.py
├── urls.py
├── requirements.txt
├── README.md
├── requests.log
├── chats/
│   ├── __init__.py
│   ├── middleware.py
│   ├── urls.py
│   └── views.py
└── messaging_app/
    ├── __init__.py
    ├── asgi.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

## Configuration

The middleware is configured in `settings.py`:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Custom middleware
    'chats.middleware.RequestLoggingMiddleware',
    'chats.middleware.RestrictAccessByTimeMiddleware',
    'chats.middleware.OffensiveLanguageMiddleware',
    'chats.middleware.RolepermissionMiddleware',
]
``` 