"""
Sample script to test the messaging API
Run this after setting up the project and creating users
"""

import requests
import json

# Base URL for the API
BASE_URL = 'http://localhost:8000/api'

# Test credentials (create these users first via admin or shell)
USERNAME = 'testuser1'
PASSWORD = 'testpass123'


class MessagingAPITest:
    def __init__(self):
        self.session = requests.Session()
        self.authenticated = False
    
    def login(self):
        """Login to get session authentication"""
        login_url = 'http://localhost:8000/api-auth/login/'
        
        # Get CSRF token
        response = self.session.get(login_url)
        csrf_token = response.cookies['csrftoken']
        
        # Login
        login_data = {
            'username': USERNAME,
            'password': PASSWORD,
            'csrfmiddlewaretoken': csrf_token
        }
        
        response = self.session.post(login_url, data=login_data)
        
        if response.status_code == 200:
            print("✓ Successfully logged in")
            self.authenticated = True
            return True
        else:
            print("✗ Login failed")
            return False
    
    def test_user_list(self):
        """Test listing users"""
        response = self.session.get(f'{BASE_URL}/users/')
        
        if response.status_code == 200:
            users = response.json()
            print(f"✓ Found {users['count']} users")
            return users
        else:
            print(f"✗ Failed to get users: {response.status_code}")
            return None
    
    def test_create_conversation(self, participant_ids=None):
        """Test creating a conversation"""
        data = {
            'participant_ids': participant_ids or []
        }
        
        response = self.session.post(
            f'{BASE_URL}/conversations/',
            json=data,
            headers={'X-CSRFToken': self.session.cookies.get('csrftoken')}
        )
        
        if response.status_code == 201:
            conversation = response.json()
            print(f"✓ Created conversation: {conversation['conversation_id']}")
            return conversation
        else:
            print(f"✗ Failed to create conversation: {response.status_code}")
            print(response.text)
            return None
    
    def test_send_message(self, conversation_id, message_body):
        """Test sending a message"""
        data = {
            'conversation_id': conversation_id,
            'message_body': message_body
        }
        
        response = self.session.post(
            f'{BASE_URL}/messages/',
            json=data,
            headers={'X-CSRFToken': self.session.cookies.get('csrftoken')}
        )
        
        if response.status_code == 201:
            message = response.json()
            print(f"✓ Sent message: {message['message_id']}")
            return message
        else:
            print(f"✗ Failed to send message: {response.status_code}")
            print(response.text)
            return None
    
    def test_get_conversations(self):
        """Test getting user's conversations"""
        response = self.session.get(f'{BASE_URL}/conversations/')
        
        if response.status_code == 200:
            conversations = response.json()
            print(f"✓ Found {conversations['count']} conversations")
            return conversations
        else:
            print(f"✗ Failed to get conversations: {response.status_code}")
            return None
    
    def test_get_messages(self, conversation_id=None):
        """Test getting messages"""
        url = f'{BASE_URL}/messages/'
        if conversation_id:
            url += f'?conversation_id={conversation_id}'
        
        response = self.session.get(url)
        
        if response.status_code == 200:
            messages = response.json()
            print(f"✓ Found {messages['count']} messages")
            return messages
        else:
            print(f"✗ Failed to get messages: {response.status_code}")
            return None
    
    def run_all_tests(self):
        """Run all API tests"""
        print("\n=== Starting API Tests ===\n")
        
        # 1. Login
        if not self.login():
            print("Cannot proceed without authentication")
            return
        
        print("\n--- Testing User Endpoints ---")
        users = self.test_user_list()
        
        print("\n--- Testing Conversation Creation ---")
        conversation = self.test_create_conversation()
        
        if conversation:
            conversation_id = conversation['conversation_id']
            
            print("\n--- Testing Message Sending ---")
            self.test_send_message(conversation_id, "Hello, this is a test message!")
            self.test_send_message(conversation_id, "Another test message")
            
            print("\n--- Testing Message Retrieval ---")
            self.test_get_messages(conversation_id)
        
        print("\n--- Testing Conversation List ---")
        self.test_get_conversations()
        
        print("\n=== Tests Complete ===\n")


if __name__ == '__main__':
    # Make sure the server is running before running tests
    print("Make sure the Django server is running on http://localhost:8000")
    print("And that you have created a test user with username 'testuser1' and password 'testpass123'")
    input("Press Enter to continue...")
    
    tester = MessagingAPITest()
    tester.run_all_tests()