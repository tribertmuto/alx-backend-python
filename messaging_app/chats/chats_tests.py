from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import User, Conversation, Message

User = get_user_model()

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='guest',
            phone_number='+1234567890'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.role, 'guest')
        self.assertEqual(self.user.phone_number, '+1234567890')
        self.assertTrue(self.user.user_id)

    def test_user_str_method(self):
        self.assertEqual(str(self.user), 'testuser')

class ConversationModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='pass123',
            role='guest'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='pass123',
            role='host'
        )
        self.conversation = Conversation.objects.create()
        self.conversation.participants.add(self.user1, self.user2)

    def test_conversation_creation(self):
        self.assertTrue(self.conversation.conversation_id)
        self.assertEqual(self.conversation.participants.count(), 2)
        self.assertTrue(self.conversation.created_at)

class MessageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='sender',
            email='sender@example.com',
            password='pass123',
            role='guest'
        )
        self.conversation = Conversation.objects.create()
        self.conversation.participants.add(self.user)
        self.message = Message.objects.create(
            sender=self.user,
            conversation=self.conversation,
            message_body='Hello, world!'
        )

    def test_message_creation(self):
        self.assertEqual(self.message.sender, self.user)
        self.assertEqual(self.message.conversation, self.conversation)
        self.assertEqual(self.message.message_body, 'Hello, world!')
        self.assertTrue(self.message.message_id)
        self.assertTrue(self.message.sent_at)

class ConversationAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='guest'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        self.conversation = Conversation.objects.create()
        self.conversation.participants.add(self.user)

    def test_get_conversations(self):
        url = reverse('conversation-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_conversation(self):
        url = reverse('conversation-list')
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class MessageAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='guest'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        self.conversation = Conversation.objects.create()
        self.conversation.participants.add(self.user)
        
        self.message = Message.objects.create(
            sender=self.user,
            conversation=self.conversation,
            message_body='Test message'
        )

    def test_get_messages(self):
        url = reverse('message-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_message(self):
        url = reverse('message-list')
        data = {
            'conversation': self.conversation.conversation_id,
            'message_body': 'New test message'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message_body'], 'New test message')

class AuthenticationTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='guest'
        )

    def test_unauthenticated_access(self):
        # Test that unauthenticated users cannot access the API
        url = reverse('conversation-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_access(self):
        # Test that authenticated users can access the API
        self.client.force_authenticate(user=self.user)
        url = reverse('conversation-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        from django.test import TestCase
from .models import User

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(username='testuser', password='testpass', role='guest')
        self.assertEqual(user.username, 'testuser')
