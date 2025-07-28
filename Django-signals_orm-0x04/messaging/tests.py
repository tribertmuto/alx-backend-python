from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.cache import cache
from .models import Message, Notification, MessageHistory
from .signals import create_notification_for_new_message, log_message_edit


class MessageModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass123')
        self.user2 = User.objects.create_user(username='user2', password='testpass123')

    def test_message_creation(self):
        """Test creating a message."""
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Hello, this is a test message!'
        )
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.receiver, self.user2)
        self.assertEqual(message.content, 'Hello, this is a test message!')
        self.assertFalse(message.read)
        self.assertFalse(message.edited)

    def test_message_str(self):
        """Test message string representation."""
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Test message'
        )
        expected = f"{self.user1.username} to {self.user2.username}: Test message"
        self.assertEqual(str(message), expected)

    def test_threaded_message(self):
        """Test creating threaded messages."""
        parent_message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Original message'
        )
        
        reply = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content='Reply to original',
            parent_message=parent_message
        )
        
        self.assertEqual(reply.parent_message, parent_message)
        self.assertIn(reply, parent_message.replies.all())


class NotificationModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass123')
        self.user2 = User.objects.create_user(username='user2', password='testpass123')
        self.message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Test message'
        )

    def test_notification_creation(self):
        """Test creating a notification."""
        notification = Notification.objects.create(
            user=self.user2,
            message=self.message
        )
        self.assertEqual(notification.user, self.user2)
        self.assertEqual(notification.message, self.message)
        self.assertFalse(notification.read)


class MessageHistoryModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass123')
        self.user2 = User.objects.create_user(username='user2', password='testpass123')
        self.message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Original content'
        )

    def test_message_history_creation(self):
        """Test creating message history."""
        history = MessageHistory.objects.create(
            message=self.message,
            old_content='Old content',
            edited_by=self.user1
        )
        self.assertEqual(history.message, self.message)
        self.assertEqual(history.old_content, 'Old content')
        self.assertEqual(history.edited_by, self.user1)


class UnreadMessagesManagerTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass123')
        self.user2 = User.objects.create_user(username='user2', password='testpass123')
        
        # Create some messages
        Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Unread message 1',
            read=False
        )
        Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Read message',
            read=True
        )
        Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content='Unread message 2',
            read=False
        )

    def test_unread_messages_manager(self):
        """Test the custom unread messages manager."""
        unread_messages = Message.unread.unread_for_user(self.user2)
        self.assertEqual(unread_messages.count(), 1)
        self.assertEqual(unread_messages.first().content, 'Unread message 1')


class SignalTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass123')
        self.user2 = User.objects.create_user(username='user2', password='testpass123')

    def test_notification_signal(self):
        """Test that notification is created when message is created."""
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Test message'
        )
        
        # Check that notification was created
        notification = Notification.objects.filter(user=self.user2, message=message)
        self.assertTrue(notification.exists())
        self.assertEqual(notification.count(), 1)

    def test_no_notification_for_self_message(self):
        """Test that no notification is created when sender sends to self."""
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user1,
            content='Self message'
        )
        
        # Check that no notification was created
        notification = Notification.objects.filter(user=self.user1, message=message)
        self.assertFalse(notification.exists())

    def test_message_edit_signal(self):
        """Test that message history is created when message is edited."""
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Original content'
        )
        
        # Edit the message
        message.content = 'Edited content'
        message.save()
        
        # Check that history was created
        history = MessageHistory.objects.filter(message=message)
        self.assertTrue(history.exists())
        self.assertEqual(history.first().old_content, 'Original content')
        self.assertTrue(message.edited)


class ViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='testpass123')
        self.user2 = User.objects.create_user(username='user2', password='testpass123')
        
        # Create some test messages
        Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Test message 1'
        )
        Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content='Test message 2'
        )

    def test_conversation_list_view(self):
        """Test conversation list view with caching."""
        self.client.login(username='user1', password='testpass123')
        
        # Clear cache first
        cache.clear()
        
        response = self.client.get(reverse('messaging:conversation_list'))
        self.assertEqual(response.status_code, 200)
        
        # Test that the view is cached
        response2 = self.client.get(reverse('messaging:conversation_list'))
        self.assertEqual(response2.status_code, 200)

    def test_conversation_detail_view(self):
        """Test conversation detail view."""
        self.client.login(username='user1', password='testpass123')
        
        response = self.client.get(reverse('messaging:conversation_detail', args=[self.user2.id]))
        self.assertEqual(response.status_code, 200)

    def test_send_message_view(self):
        """Test sending a message."""
        self.client.login(username='user1', password='testpass123')
        
        response = self.client.post(
            reverse('messaging:send_message', args=[self.user2.id]),
            {'content': 'New test message'}
        )
        self.assertEqual(response.status_code, 200)
        
        # Check that message was created
        message = Message.objects.filter(
            sender=self.user1,
            receiver=self.user2,
            content='New test message'
        )
        self.assertTrue(message.exists())

    def test_edit_message_view(self):
        """Test editing a message."""
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Original content'
        )
        
        self.client.login(username='user1', password='testpass123')
        
        response = self.client.post(
            reverse('messaging:edit_message', args=[message.id]),
            {'content': 'Edited content'}
        )
        self.assertEqual(response.status_code, 200)
        
        # Check that message was updated
        message.refresh_from_db()
        self.assertEqual(message.content, 'Edited content')
        self.assertTrue(message.edited)

    def test_notifications_view(self):
        """Test notifications view."""
        self.client.login(username='user2', password='testpass123')
        
        response = self.client.get(reverse('messaging:notifications'))
        self.assertEqual(response.status_code, 200)

    def test_unread_messages_view(self):
        """Test unread messages view."""
        self.client.login(username='user2', password='testpass123')
        
        response = self.client.get(reverse('messaging:unread_messages'))
        self.assertEqual(response.status_code, 200)

    def test_threaded_conversation_view(self):
        """Test threaded conversation view."""
        parent_message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Parent message'
        )
        
        reply = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content='Reply message',
            parent_message=parent_message
        )
        
        self.client.login(username='user1', password='testpass123')
        
        response = self.client.get(reverse('messaging:threaded_conversation', args=[parent_message.id]))
        self.assertEqual(response.status_code, 200)


class UserDeletionTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass123')
        self.user2 = User.objects.create_user(username='user2', password='testpass123')
        
        # Create messages and notifications
        message1 = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Message from user1'
        )
        message2 = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content='Message to user1'
        )
        
        # Create message history entries
        MessageHistory.objects.create(
            message=message1,
            old_content='Original content',
            edited_by=self.user1
        )
        MessageHistory.objects.create(
            message=message2,
            old_content='Original content',
            edited_by=self.user2
        )
        
        Notification.objects.create(user=self.user2, message=message1)
        Notification.objects.create(user=self.user1, message=message2)

    def test_user_deletion_cascade(self):
        """Test that user deletion cascades to related data."""
        # Delete user1
        self.user1.delete()
        
        # Check that user1's messages are deleted
        self.assertFalse(Message.objects.filter(sender=self.user1).exists())
        self.assertFalse(Message.objects.filter(receiver=self.user1).exists())
        
        # Check that notifications for user1 are deleted
        self.assertFalse(Notification.objects.filter(user=self.user1).exists())
        
        # Check that message histories where user1 was the editor are deleted
        self.assertFalse(MessageHistory.objects.filter(edited_by=self.user1).exists())
        
        # Check that user2's data is still intact
        self.assertTrue(Message.objects.filter(sender=self.user2).exists())
        self.assertTrue(Notification.objects.filter(user=self.user2).exists())
        self.assertTrue(MessageHistory.objects.filter(edited_by=self.user2).exists()) 