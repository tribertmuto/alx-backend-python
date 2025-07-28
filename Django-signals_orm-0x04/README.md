# Django Signals and ORM Techniques - Messaging App

This project implements a comprehensive messaging application using Django signals and advanced ORM techniques.

## Features Implemented

### 1. Signals for User Notifications ✅
- **Message Model**: Includes sender, receiver, content, timestamp, read status, and edited flag
- **Notification Model**: Stores notifications linking users to messages
- **Signal Implementation**: `post_save` signal automatically creates notifications when new messages are created
- **Location**: `messaging/models.py`, `messaging/signals.py`

### 2. Signal for Logging Message Edits ✅
- **MessageHistory Model**: Stores edit history with old content and edit metadata
- **Pre-save Signal**: Logs old content before message updates
- **Edit Tracking**: Messages marked as edited when content changes
- **History Display**: UI shows edit history for messages
- **Location**: `messaging/models.py`, `messaging/signals.py`, `messaging/views.py`

### 3. Signals for Deleting User-Related Data ✅
- **User Deletion View**: Allows users to delete their accounts
- **CASCADE Deletion**: Foreign key constraints automatically clean up related data
- **Signal Handling**: `post_delete` signal for custom cleanup logic
- **Location**: `messaging/views.py`, `messaging/signals.py`

### 4. Advanced ORM Techniques for Threaded Conversations ✅
- **Self-Referential Foreign Key**: `parent_message` field for message replies
- **Optimized Queries**: Uses `select_related` and `prefetch_related` for efficient data retrieval
- **Recursive Threading**: `get_thread()` method retrieves entire conversation threads
- **Threaded Display**: UI shows messages in threaded format
- **Location**: `messaging/models.py`, `messaging/views.py`

### 5. Custom ORM Manager for Unread Messages ✅
- **UnreadMessagesManager**: Custom manager with `for_user()` method
- **Optimized Queries**: Uses `select_related` and `only()` for performance
- **Unread Filtering**: Filters messages by read status and user
- **Location**: `messaging/models.py`, `messaging/views.py`

### 6. Basic View Caching ✅
- **Cache Configuration**: LocMemCache with unique location
- **Cache Decorator**: `@cache_page(60)` on conversation list view
- **60-Second Timeout**: Cache expires after 60 seconds
- **Location**: `messaging_app/settings.py`, `messaging/views.py`

## Project Structure

```
Django-signals_orm-0x04/
├── messaging_app/
│   ├── __init__.py
│   ├── settings.py          # Cache configuration
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── messaging/
│   ├── __init__.py
│   ├── apps.py             # Signal registration
│   ├── models.py           # All models with custom manager
│   ├── signals.py          # All signal implementations
│   ├── views.py            # Views with caching
│   ├── urls.py             # URL patterns
│   ├── admin.py            # Admin interface
│   ├── tests.py            # Comprehensive tests
│   └── templates/
│       └── messaging/
│           ├── base.html
│           ├── conversation_list.html
│           ├── conversation_detail.html
│           ├── notifications.html
│           ├── unread_messages.html
│           ├── message_history.html
│           ├── delete_account.html
│           └── threaded_conversation.html
├── manage.py
├── requirements.txt
└── README.md
```

## Models

### Message Model
- `sender`: ForeignKey to User
- `receiver`: ForeignKey to User  
- `content`: TextField
- `timestamp`: DateTimeField (auto_now_add)
- `read`: BooleanField (default=False)
- `edited`: BooleanField (default=False)
- `parent_message`: Self-referential ForeignKey for replies

### Notification Model
- `user`: ForeignKey to User
- `message`: ForeignKey to Message
- `timestamp`: DateTimeField (auto_now_add)
- `read`: BooleanField (default=False)

### MessageHistory Model
- `message`: ForeignKey to Message
- `old_content`: TextField
- `edited_at`: DateTimeField (auto_now_add)
- `edited_by`: ForeignKey to User

## Signals

### 1. Notification Signal (`post_save`)
- Triggers when new Message is created
- Creates notification for receiver
- Excludes self-messages

### 2. Edit Logging Signal (`pre_save`)
- Captures old content before message update
- Creates MessageHistory entry
- Sets edited flag to True

### 3. User Deletion Signal (`post_delete`)
- Handles cleanup of user-related data
- CASCADE relationships handle most cleanup automatically

## Custom Manager

### UnreadMessagesManager
- `for_user(user)`: Returns unread messages for specific user
- Optimized with `select_related` and `only()`
- Filters by `read=False` and `receiver=user`

## Views with Caching

### Cached Views
- `conversation_list`: Cached for 60 seconds
- Uses `@cache_page(60)` decorator

### Other Views
- `conversation_detail`: Shows conversation with specific user
- `send_message`: Handles message creation
- `edit_message`: Handles message editing
- `message_history`: Shows edit history
- `notifications`: Shows user notifications
- `unread_messages`: Shows unread messages using custom manager
- `delete_user_account`: Handles account deletion
- `threaded_conversation`: Shows threaded conversation

## Testing

Comprehensive test suite covering:
- Model creation and relationships
- Signal functionality
- Custom manager behavior
- View functionality
- User deletion cascade
- Caching behavior

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

4. Run tests:
   ```bash
   python manage.py test messaging
   ```

5. Run development server:
   ```bash
   python manage.py runserver
   ```

## Key Features Demonstrated

1. **Django Signals**: Automatic notification creation and edit logging
2. **Advanced ORM**: Custom managers, optimized queries, self-referential relationships
3. **Caching**: View-level caching with configurable timeouts
4. **Threaded Conversations**: Hierarchical message structure
5. **User Management**: Account deletion with data cleanup
6. **Message History**: Complete edit tracking and history display

## Performance Optimizations

- `select_related()` for foreign key relationships
- `prefetch_related()` for reverse foreign key relationships
- `only()` to retrieve only necessary fields
- Custom manager for optimized unread message queries
- View caching to reduce database queries
- Efficient threaded conversation retrieval

This implementation demonstrates advanced Django concepts including signals, custom managers, ORM optimization, caching, and comprehensive testing. 