# Django Middleware Configuration Documentation

## Overview

This Django project implements four custom middleware classes to provide enhanced functionality for a chat application. The middleware is properly configured in `messaging_app/settings.py` and includes logging, time-based access control, rate limiting, and role-based permissions.

## Middleware Configuration

### 1. RequestLoggingMiddleware
- **Purpose**: Logs all incoming requests with user information
- **Location**: `chats/middleware.py`
- **Configuration**: Automatically logs to `requests.log` file
- **Features**:
  - Logs user (authenticated or anonymous)
  - Logs request path and method
  - Error handling with graceful fallback

### 2. RestrictAccessByTimeMiddleware
- **Purpose**: Restricts access to chat functionality based on time
- **Location**: `chats/middleware.py`
- **Configuration**: Allows access only between 6 PM and 9 PM (18:00 - 21:00)
- **Features**:
  - Time-based access control
  - Returns 403 Forbidden outside allowed hours
  - Error handling with graceful fallback

### 3. RateLimitMiddleware
- **Purpose**: Implements rate limiting for message sending
- **Location**: `chats/middleware.py`
- **Configuration**: Limits to 5 messages per minute per IP address
- **Features**:
  - IP-based rate limiting
  - Automatic cleanup of old entries
  - Returns 403 Forbidden when limit exceeded

### 4. RolepermissionMiddleware
- **Purpose**: Enforces role-based access control for admin functions
- **Location**: `chats/middleware.py`
- **Configuration**: Protects `/api/delete/` and `/api/manage/` endpoints
- **Features**:
  - Requires authentication
  - Checks user role (admin or moderator)
  - Returns 403 Forbidden for unauthorized access

## Settings Configuration

The middleware is configured in `messaging_app/settings.py`:

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
    'chats.middleware.RateLimitMiddleware',
    'chats.middleware.RolepermissionMiddleware',
]
```

## Verification Commands

### 1. Check Middleware Configuration
```bash
python test_middleware.py
```

This script verifies:
- Settings can be imported successfully
- All custom middleware is found in settings
- All middleware classes can be instantiated and called

### 2. Django System Check
```bash
python manage.py check
```

This command checks for any configuration issues in the Django project.

### 3. Test Middleware Functionality

#### Test Request Logging
```bash
curl http://localhost:8000/api/
```
Check `requests.log` file for logged requests.

#### Test Time Restriction
```bash
curl http://localhost:8000/api/
```
Returns 403 Forbidden outside 6 PM - 9 PM window.

#### Test Rate Limiting
```bash
# Send multiple POST requests quickly
curl -X POST http://localhost:8000/api/send/ -H "Content-Type: application/json" -d '{"message":"test"}'
```
Returns 403 Forbidden after 5 requests within 1 minute.

#### Test Role Permissions
```bash
curl http://localhost:8000/api/manage/
```
Returns 403 Forbidden for non-admin/moderator users.

## Project Structure

```
Django-Middleware-0x03/
├── messaging_app/
│   ├── settings.py          # Main settings file with middleware configuration
│   ├── urls.py              # URL configuration
│   └── wsgi.py              # WSGI application
├── chats/
│   ├── middleware.py        # Custom middleware implementations
│   ├── models.py            # User and ChatMessage models
│   ├── views.py             # API views
│   └── urls.py              # Chat app URLs
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── test_middleware.py       # Middleware verification script
└── requests.log             # Request logging output
```

## Dependencies

The project requires the following packages (see `requirements.txt`):
- Django>=4.2.0,<5.0.0
- djangorestframework>=3.14.0
- djangorestframework-simplejwt>=5.2.0
- django-filter>=23.0
- Pillow>=9.0.0
- python-decouple>=3.8

## Installation and Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run migrations:
   ```bash
   python manage.py migrate
   ```

3. Verify configuration:
   ```bash
   python test_middleware.py
   python manage.py check
   ```

4. Start development server:
   ```bash
   python manage.py runserver
   ```

## Middleware Order

The middleware is executed in the order specified in the MIDDLEWARE setting:

1. Django's built-in middleware (security, sessions, etc.)
2. Custom middleware:
   - RequestLoggingMiddleware (logs all requests)
   - RestrictAccessByTimeMiddleware (time-based access control)
   - RateLimitMiddleware (rate limiting)
   - RolepermissionMiddleware (role-based permissions)

This order ensures that:
- All requests are logged first
- Time restrictions are checked early
- Rate limiting is applied before processing
- Role permissions are checked last

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Ensure all dependencies are installed
2. **ImportError**: Check that the settings module path is correct in manage.py
3. **Middleware not found**: Verify middleware classes are properly imported
4. **Permission denied**: Check file permissions for log files

### Debug Commands

```bash
# Check Django configuration
python manage.py check --deploy

# Test specific middleware
python -c "from chats.middleware import RequestLoggingMiddleware; print('OK')"

# View current settings
python manage.py shell -c "from django.conf import settings; print(settings.MIDDLEWARE)"
```

## Security Considerations

- The middleware includes proper error handling to prevent information leakage
- Rate limiting helps prevent abuse
- Role-based access control ensures proper authorization
- All middleware returns appropriate HTTP status codes
- Logging is configured to avoid sensitive data exposure 