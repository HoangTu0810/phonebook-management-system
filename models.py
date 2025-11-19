import json
import hashlib
import datetime
from typing import List, Dict, Optional

class User:
    def __init__(self, user_id: int, username: str, email: str, password: str, role: str = "user", 
                 created_at: str = None, last_login: str = None, is_active: bool = True):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.reset_token = None
        self.reset_token_expiry = None
        
        if password.startswith('$SHA$') or len(password) == 64:
            self.password_hash = password
        else:
            self.password_hash = self._hash_password(password)
        
        self.role = role
        self.created_at = created_at or datetime.datetime.now().isoformat()
        self.last_login = last_login
        self.is_active = is_active
    
    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str) -> bool:
        return self.password_hash == self._hash_password(password)
    
    def update_profile(self, **kwargs):
        allowed_fields = ['username', 'email']
        for field, value in kwargs.items():
            if field in allowed_fields:
                setattr(self, field, value)
    
    def to_dict(self):
        data = {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash,
            'role': self.role,
            'created_at': self.created_at,
            'last_login': self.last_login,
            'is_active': self.is_active
        }
        if hasattr(self, 'reset_token') and self.reset_token:
            data['reset_token'] = self.reset_token
        if hasattr(self, 'reset_token_expiry') and self.reset_token_expiry:
            data['reset_token_expiry'] = self.reset_token_expiry
        return data

    @classmethod
    def from_dict(cls, data: dict):
        password = data.get('password_hash') or data.get('password')
        if not password:
            raise ValueError("Missing password in user data")
        
        user = cls(
            user_id=data['user_id'],
            username=data['username'],
            email=data['email'],
            password=password,
            role=data.get('role', 'user'),
            created_at=data.get('created_at'),
            last_login=data.get('last_login'),
            is_active=data.get('is_active', True)
        )
        
        if 'reset_token' in data:
            user.reset_token = data['reset_token']
        if 'reset_token_expiry' in data:
            user.reset_token_expiry = data['reset_token_expiry']
        
        return user

class Contact:
    def __init__(self, contact_id: int, user_id: int, first_name: str, last_name: str, 
                 phone: str, email: str = "", address: str = "", group: str = "General", 
                 notes: str = "", is_favorite: bool = False, is_blocked: bool = False,
                 created_at: str = None, updated_at: str = None):
        self.contact_id = contact_id
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.address = address
        self.group = group
        self.notes = notes
        self.is_favorite = is_favorite
        self.is_blocked = is_blocked
        self.created_at = created_at or datetime.datetime.now().isoformat()
        self.updated_at = updated_at or self.created_at
    
    def update_contact(self, **kwargs):
        allowed_fields = ['first_name', 'last_name', 'phone', 'email', 'address', 'group', 'notes']
        for field, value in kwargs.items():
            if field in allowed_fields:
                setattr(self, field, value)
        self.updated_at = datetime.datetime.now().isoformat()
    
    def mark_as_favorite(self):
        self.is_favorite = True
    
    def unmark_favorite(self):
        self.is_favorite = False
    
    def block_contact(self):
        self.is_blocked = True
    
    def unblock_contact(self):
        self.is_blocked = False
    
    def to_dict(self):
        return {
            'contact_id': self.contact_id,
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'group': self.group,
            'notes': self.notes,
            'is_favorite': self.is_favorite,
            'is_blocked': self.is_blocked,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            contact_id=data['contact_id'],
            user_id=data['user_id'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone=data['phone'],
            email=data.get('email', ''),
            address=data.get('address', ''),
            group=data.get('group', 'General'),
            notes=data.get('notes', ''),
            is_favorite=data.get('is_favorite', False),
            is_blocked=data.get('is_blocked', False),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )