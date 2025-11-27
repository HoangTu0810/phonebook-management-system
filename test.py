"""
Test script for PhoneBook Management System
Run this file to test all functionalities of the application
"""

import os
import sys
import unittest
import tempfile
import shutil
from unittest.mock import patch
from io import StringIO

# Add the current directory to Python path to import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from system import PhoneBookSystem
from models import User, Contact
from ui import PhoneBookUI

class TestPhoneBookSystem(unittest.TestCase):
    """Test cases for PhoneBookSystem class"""
    
    def setUp(self):
        """Set up test environment before each test"""
        self.test_dir = tempfile.mkdtemp()
        self.system = PhoneBookSystem(data_dir=self.test_dir)
    
    def tearDown(self):
        """Clean up after each test"""
        shutil.rmtree(self.test_dir)
    
    def test_initialization(self):
        """Test system initialization"""
        self.assertEqual(len(self.system.users), 0)
        self.assertEqual(len(self.system.contacts), 0)
        self.assertIsNone(self.system.current_user)
    
    def test_register_user(self):
        """Test user registration"""
        # Test successful registration
        result = self.system.register_user("testuser", "test@example.com", "password123")
        self.assertTrue(result)
        self.assertEqual(len(self.system.users), 1)
        
        # Test duplicate email registration
        result = self.system.register_user("anotheruser", "test@example.com", "password456")
        self.assertFalse(result)
        self.assertEqual(len(self.system.users), 1)
    
    def test_login(self):
        """Test user login"""
        # Register a user first
        self.system.register_user("testuser", "test@example.com", "password123")
        
        # Test successful login
        result = self.system.login("test@example.com", "password123")
        self.assertTrue(result)
        self.assertIsNotNone(self.system.current_user)
        self.assertEqual(self.system.current_user.email, "test@example.com")
        
        # Test wrong password
        result = self.system.login("test@example.com", "wrongpassword")
        self.assertFalse(result)
        
        # Test non-existent email
        result = self.system.login("nonexistent@example.com", "password123")
        self.assertFalse(result)
    
    def test_add_contact(self):
        """Test adding contacts"""
        # Register and login first
        self.system.register_user("testuser", "test@example.com", "password123")
        self.system.login("test@example.com", "password123")
        
        # Test adding contact
        result = self.system.add_contact("John", "Doe", "1234567890")
        self.assertTrue(result)
        self.assertEqual(len(self.system.contacts), 1)
        
        contact = self.system.contacts[0]
        self.assertEqual(contact.first_name, "John")
        self.assertEqual(contact.last_name, "Doe")
        self.assertEqual(contact.phone, "1234567890")
    
    def test_edit_contact(self):
        """Test editing contacts"""
        # Setup
        self.system.register_user("testuser", "test@example.com", "password123")
        self.system.login("test@example.com", "password123")
        self.system.add_contact("John", "Doe", "1234567890")
        contact_id = self.system.contacts[0].contact_id
        
        # Test editing contact
        result = self.system.edit_contact(contact_id, first_name="Jane", phone="0987654321")
        self.assertTrue(result)
        
        contact = self.system.get_contact_by_id(contact_id)
        self.assertEqual(contact.first_name, "Jane")
        self.assertEqual(contact.phone, "0987654321")
    
    def test_delete_contact(self):
        """Test deleting contacts"""
        # Setup
        self.system.register_user("testuser", "test@example.com", "password123")
        self.system.login("test@example.com", "password123")
        self.system.add_contact("John", "Doe", "1234567890")
        contact_id = self.system.contacts[0].contact_id
        
        # Test deleting contact
        result = self.system.delete_contact(contact_id)
        self.assertTrue(result)
        self.assertEqual(len(self.system.contacts), 0)
    
    def test_search_contacts(self):
        """Test contact search functionality"""
        # Setup
        self.system.register_user("testuser", "test@example.com", "password123")
        self.system.login("test@example.com", "password123")
        self.system.add_contact("John", "Doe", "1234567890", email="john@example.com")
        self.system.add_contact("Jane", "Smith", "0987654321", email="jane@example.com")
        
        # Test search by first name
        results = self.system.search_contacts("John")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].first_name, "John")
        
        # Test search by last name
        results = self.system.search_contacts("Doe")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].last_name, "Doe")
        
        # Test search by phone
        results = self.system.search_contacts("123456")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].phone, "1234567890")
        
        # Test search by email
        results = self.system.search_contacts("jane@example")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].email, "jane@example.com")
    
    def test_toggle_favorite_contact(self):
        """Test toggling favorite status"""
        # Setup
        self.system.register_user("testuser", "test@example.com", "password123")
        self.system.login("test@example.com", "password123")
        self.system.add_contact("John", "Doe", "1234567890")
        contact_id = self.system.contacts[0].contact_id
        
        # Test marking as favorite
        result = self.system.toggle_favorite_contact(contact_id)
        self.assertTrue(result)
        self.assertTrue(self.system.contacts[0].is_favorite)
        
        # Test unmarking favorite
        result = self.system.toggle_favorite_contact(contact_id)
        self.assertFalse(result)
        self.assertFalse(self.system.contacts[0].is_favorite)
    
    def test_password_reset(self):
        """Test password reset functionality"""
        # Setup
        self.system.register_user("testuser", "test@example.com", "password123")
        
        # Test requesting reset token
        token = self.system.request_password_reset("test@example.com")
        self.assertIsNotNone(token)
        
        # Test validating token
        self.assertTrue(self.system.validate_reset_token(token))
        
        # Test resetting password
        result = self.system.reset_password(token, "newpassword456")
        self.assertTrue(result)
        
        # Test login with new password
        result = self.system.login("test@example.com", "newpassword456")
        self.assertTrue(result)
    
    def test_export_import_contacts(self):
        """Test export and import functionality"""
        # Setup
        self.system.register_user("testuser", "test@example.com", "password123")
        self.system.login("test@example.com", "password123")
        self.system.add_contact("John", "Doe", "1234567890", email="john@example.com")
        
        # Test export
        export_file = os.path.join(self.test_dir, "export_test.txt")
        result = self.system.export_contacts_to_txt(export_file)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(export_file))
        
        # Clear contacts and test import
        self.system.contacts.clear()
        self.system.next_contact_id = 1
        
        results = self.system.import_contacts_from_txt(export_file)
        self.assertEqual(results["success"], 1)
        self.assertEqual(len(self.system.contacts), 1)
        self.assertEqual(self.system.contacts[0].first_name, "John")

class TestModels(unittest.TestCase):
    """Test cases for models (User and Contact)"""
    
    def test_user_creation(self):
        """Test User model creation and methods"""
        user = User(1, "testuser", "test@example.com", "password123")
        
        self.assertEqual(user.user_id, 1)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.verify_password("password123"))
        self.assertFalse(user.verify_password("wrongpassword"))
    
    def test_user_update_profile(self):
        """Test user profile updates"""
        user = User(1, "testuser", "test@example.com", "password123")
        
        user.update_profile(username="newuser", email="new@example.com")
        self.assertEqual(user.username, "newuser")
        self.assertEqual(user.email, "new@example.com")
    
    def test_contact_creation(self):
        """Test Contact model creation and methods"""
        contact = Contact(1, 1, "John", "Doe", "1234567890", 
                         email="john@example.com", group="Friends")
        
        self.assertEqual(contact.contact_id, 1)
        self.assertEqual(contact.first_name, "John")
        self.assertEqual(contact.last_name, "Doe")
        self.assertEqual(contact.phone, "1234567890")
        self.assertEqual(contact.email, "john@example.com")
        self.assertEqual(contact.group, "Friends")
    
    def test_contact_update(self):
        """Test contact updates"""
        contact = Contact(1, 1, "John", "Doe", "1234567890")
        
        contact.update_contact(first_name="Jane", phone="0987654321")
        self.assertEqual(contact.first_name, "Jane")
        self.assertEqual(contact.phone, "0987654321")
    
    def test_contact_favorite_toggle(self):
        """Test contact favorite toggling"""
        contact = Contact(1, 1, "John", "Doe", "1234567890")
        
        self.assertFalse(contact.is_favorite)
        contact.mark_as_favorite()
        self.assertTrue(contact.is_favorite)
        contact.unmark_favorite()
        self.assertFalse(contact.is_favorite)

class TestUI(unittest.TestCase):
    """Test cases for UI functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.system = PhoneBookSystem(data_dir=self.test_dir)
        self.ui = PhoneBookUI()
        self.ui.system = self.system
    
    def tearDown(self):
        """Clean up after tests"""
        shutil.rmtree(self.test_dir)
    
    @patch('builtins.input')
    def test_login_ui(self, mock_input):
        """Test UI login functionality"""
        # Setup
        self.system.register_user("testuser", "test@example.com", "password123")
        
        # Mock user input for login
        mock_input.side_effect = ["test@example.com", "password123"]
        
        # Redirect stdout to capture output
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.ui.login()
            output = mock_stdout.getvalue()
            
        self.assertIn("Login successful!", output)
    
    @patch('builtins.input')
    def test_register_ui(self, mock_input):
        """Test UI registration functionality"""
        # Mock user input for registration
        mock_input.side_effect = [
            "newuser", 
            "newuser@example.com", 
            "password123", 
            "password123"  # confirm password
        ]
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.ui.register()
            output = mock_stdout.getvalue()
            
        self.assertIn("Registration successful!", output)

def run_comprehensive_test():
    """Run a comprehensive test of the entire system"""
    print("=" * 60)
    print("COMPREHENSIVE PHONEBOOK SYSTEM TEST")
    print("=" * 60)
    
    # Create a temporary directory for testing
    test_dir = tempfile.mkdtemp()
    
    try:
        # Initialize system
        system = PhoneBookSystem(data_dir=test_dir)
        
        print("1. Testing User Registration...")
        # Test registration
        assert system.register_user("admin", "admin@system.com", "admin123", "admin"), "Admin registration failed"
        assert system.register_user("user1", "user1@example.com", "password123"), "User1 registration failed"
        assert system.register_user("user2", "user2@example.com", "password456"), "User2 registration failed"
        print("    User registration test passed")
        
        print("2. Testing Login...")
        # Test login
        assert system.login("admin@system.com", "admin123"), "Admin login failed"
        assert system.current_user is not None, "Current user should not be None after login"
        print("    Login test passed")
        
        print("3. Testing Contact Management...")
        # Test adding contacts
        assert system.add_contact("John", "Doe", "1234567890", email="john@doe.com"), "Add contact failed"
        assert system.add_contact("Jane", "Smith", "0987654321", group="Family"), "Add contact 2 failed"
        assert len(system.contacts) == 2, "Should have 2 contacts"
        print("    Contact addition test passed")
        
        # Test editing contact
        contact_id = system.contacts[0].contact_id
        assert system.edit_contact(contact_id, first_name="Johnny"), "Edit contact failed"
        assert system.contacts[0].first_name == "Johnny", "Contact edit didn't persist"
        print("    Contact edit test passed")
        
        # Test search
        results = system.search_contacts("Johnny")
        assert len(results) == 1, "Search should return 1 result"
        print("    Contact search test passed")
        
        # Test favorite toggle
        assert system.toggle_favorite_contact(contact_id) == True, "Toggle favorite failed"
        assert system.contacts[0].is_favorite == True, "Contact should be favorite"
        print("    Favorite toggle test passed")
        
        print("4. Testing Export/Import...")
        # Test export
        export_file = os.path.join(test_dir, "export_test.txt")
        assert system.export_contacts_to_txt(export_file), "Export failed"
        assert os.path.exists(export_file), "Export file should exist"
        print("    Export test passed")
        
        # Test import
        system.contacts.clear()
        system.next_contact_id = 1
        import_results = system.import_contacts_from_txt(export_file)
        assert import_results["success"] > 0, "Import should succeed"
        print("    Import test passed")
        
        print("5. Testing Password Reset...")
        system.logout()
        token = system.request_password_reset("admin@system.com")
        assert token is not None, "Reset token should be generated"
        assert system.validate_reset_token(token), "Token should be valid"
        assert system.reset_password(token, "newadmin123"), "Password reset should work"
        assert system.login("admin@system.com", "newadmin123"), "Should login with new password"
        print("    Password reset test passed")
        
        print("6. Testing Admin Functions...")
        users = system.get_all_users()
        assert len(users) == 3, "Should have 3 users"
        
        # Test user deactivation
        user_to_deactivate = next(user for user in users if user.email == "user2@example.com")
        assert system.deactivate_user(user_to_deactivate.user_id), "User deactivation failed"
        
        # Test backup
        backup_file = system.backup_data()
        assert "backup" in backup_file, "Backup should create a file"
        print("    Admin functions test passed")
        
        print("\n" + "=" * 60)
        print(" ALL TESTS PASSED SUCCESSFULLY! ")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up
        shutil.rmtree(test_dir)

def run_performance_test():
    """Run performance tests with large datasets"""
    print("\n" + "=" * 60)
    print("PERFORMANCE TEST")
    print("=" * 60)
    
    import time
    
    test_dir = tempfile.mkdtemp()
    
    try:
        system = PhoneBookSystem(data_dir=test_dir)
        system.register_user("perfuser", "perf@test.com", "password123")
        system.login("perf@test.com", "password123")
        
        # Test adding multiple contacts
        print("Testing performance with 100 contacts...")
        start_time = time.time()
        
        for i in range(100):
            system.add_contact(
                f"First{i}", 
                f"Last{i}", 
                f"123456{i:04d}",
                email=f"user{i}@test.com",
                group="Test"
            )
        
        add_time = time.time() - start_time
        print(f"   Added 100 contacts in {add_time:.2f} seconds")
        
        # Test search performance
        start_time = time.time()
        results = system.search_contacts("First50")
        search_time = time.time() - start_time
        print(f"   Search completed in {search_time:.4f} seconds")
        
        # Test export performance
        start_time = time.time()
        export_file = os.path.join(test_dir, "perf_export.txt")
        system.export_contacts_to_txt(export_file)
        export_time = time.time() - start_time
        print(f"   Export completed in {export_time:.2f} seconds")
        
        print("    Performance test completed")
        
    finally:
        shutil.rmtree(test_dir)

if __name__ == "__main__":
    # Run unit tests
    print("Running unit tests...")
    unittest.main(exit=False, verbosity=2)
    
    # Run comprehensive test
    run_comprehensive_test()
    
    # Run performance test
    run_performance_test()
    
    print("\n" + "=" * 60)
    print("TESTING COMPLETED")
    print("=" * 60)