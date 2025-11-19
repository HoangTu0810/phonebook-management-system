import os
import csv
import random
import string
import datetime
from typing import List, Dict, Optional
from models import User, Contact

class PhoneBookSystem:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.users_file = os.path.join(data_dir, "users.txt")  # Đổi thành .txt
        self.contacts_file = os.path.join(data_dir, "contacts.txt")  # Đổi thành .txt
        self.backups_dir = os.path.join(data_dir, "backups")
        
        os.makedirs(data_dir, exist_ok=True)
        os.makedirs(self.backups_dir, exist_ok=True)
        
        self.current_user = None
        self.users = self._load_users()
        self.contacts = self._load_contacts()
        
        self.next_user_id = max([user.user_id for user in self.users] + [0]) + 1
        self.next_contact_id = max([contact.contact_id for contact in self.contacts] + [0]) + 1
    
    def _load_users(self) -> List[User]:
        if os.path.exists(self.users_file):
            try:
                users = []
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    
                    for line in lines:
                        line = line.strip()
                        if not line or line.startswith('#'):
                            continue
                            
                        try:
                            # Định dạng: user_id|username|email|password_hash|role|created_at|last_login|is_active|reset_token|reset_token_expiry
                            parts = line.split('|')
                            if len(parts) < 7:
                                continue
                                
                            user_data = {
                                'user_id': int(parts[0]),
                                'username': parts[1],
                                'email': parts[2],
                                'password_hash': parts[3],
                                'role': parts[4],
                                'created_at': parts[5] if parts[5] != 'None' else None,
                                'last_login': parts[6] if len(parts) > 6 and parts[6] != 'None' else None,
                                'is_active': parts[7].lower() == 'true' if len(parts) > 7 else True
                            }
                            
                            if len(parts) > 8 and parts[8] != 'None':
                                user_data['reset_token'] = parts[8]
                            if len(parts) > 9 and parts[9] != 'None':
                                user_data['reset_token_expiry'] = parts[9]
                                
                            user = User.from_dict(user_data)
                            users.append(user)
                            
                        except Exception as e:
                            print(f"Error loading user from line: {e}")
                            continue
                            
                return users
            except Exception as e:
                print(f"Error reading users file: {e}")
                return []
        return []
    
    def _load_contacts(self) -> List[Contact]:
        if os.path.exists(self.contacts_file):
            try:
                contacts = []
                with open(self.contacts_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    
                    for line in lines:
                        line = line.strip()
                        if not line or line.startswith('#'):
                            continue
                            
                        try:
                            # Định dạng: contact_id|user_id|first_name|last_name|phone|email|address|group|notes|is_favorite|is_blocked|created_at|updated_at
                            parts = line.split('|')
                            if len(parts) < 5:
                                continue
                                
                            contact_data = {
                                'contact_id': int(parts[0]),
                                'user_id': int(parts[1]),
                                'first_name': parts[2],
                                'last_name': parts[3],
                                'phone': parts[4],
                                'email': parts[5] if len(parts) > 5 else '',
                                'address': parts[6] if len(parts) > 6 else '',
                                'group': parts[7] if len(parts) > 7 else 'General',
                                'notes': parts[8] if len(parts) > 8 else '',
                                'is_favorite': parts[9].lower() == 'true' if len(parts) > 9 else False,
                                'is_blocked': parts[10].lower() == 'true' if len(parts) > 10 else False,
                                'created_at': parts[11] if len(parts) > 11 and parts[11] != 'None' else None,
                                'updated_at': parts[12] if len(parts) > 12 and parts[12] != 'None' else None
                            }
                            
                            contact = Contact.from_dict(contact_data)
                            contacts.append(contact)
                            
                        except Exception as e:
                            print(f"Error loading contact from line: {e}")
                            continue
                            
                return contacts
            except Exception as e:
                print(f"Error reading contacts file: {e}")
                return []
        return []
    
    def _save_users(self):
        try:
            with open(self.users_file, 'w', encoding='utf-8') as f:
                f.write("# PhoneBook Users Data\n")
                f.write("# Format: user_id|username|email|password_hash|role|created_at|last_login|is_active|reset_token|reset_token_expiry\n")
                
                for user in self.users:
                    user_dict = user.to_dict()
                    
                    # Chuẩn bị các giá trị, thay None bằng chuỗi 'None'
                    reset_token = user_dict.get('reset_token', 'None')
                    reset_token_expiry = user_dict.get('reset_token_expiry', 'None')
                    last_login = user_dict.get('last_login', 'None')
                    
                    line = f"{user_dict['user_id']}|{user_dict['username']}|{user_dict['email']}|{user_dict['password_hash']}|{user_dict['role']}|{user_dict['created_at']}|{last_login}|{user_dict['is_active']}|{reset_token}|{reset_token_expiry}\n"
                    f.write(line)
                    
        except Exception as e:
            print(f"Error saving users: {e}")
    
    def _save_contacts(self):
        try:
            with open(self.contacts_file, 'w', encoding='utf-8') as f:
                f.write("# PhoneBook Contacts Data\n")
                f.write("# Format: contact_id|user_id|first_name|last_name|phone|email|address|group|notes|is_favorite|is_blocked|created_at|updated_at\n")
                
                for contact in self.contacts:
                    contact_dict = contact.to_dict()
                    
                    line = f"{contact_dict['contact_id']}|{contact_dict['user_id']}|{contact_dict['first_name']}|{contact_dict['last_name']}|{contact_dict['phone']}|{contact_dict['email']}|{contact_dict['address']}|{contact_dict['group']}|{contact_dict['notes']}|{contact_dict['is_favorite']}|{contact_dict['is_blocked']}|{contact_dict['created_at']}|{contact_dict['updated_at']}\n"
                    f.write(line)
                    
        except Exception as e:
            print(f"Error saving contacts: {e}")
    
    def register_user(self, username: str, email: str, password: str, role: str = "user") -> bool:
        if any(user.email == email for user in self.users):
            return False
        
        new_user = User(self.next_user_id, username, email, password, role)
        self.users.append(new_user)
        self.next_user_id += 1
        self._save_users()
        return True
    
    def login(self, email: str, password: str) -> bool:
        for user in self.users:
            if user.email == email and user.verify_password(password) and user.is_active:
                user.last_login = datetime.datetime.now().isoformat()
                self.current_user = user
                self._save_users()
                return True
        return False
    
    def generate_reset_token(self) -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    
    def request_password_reset(self, email: str) -> Optional[str]:
        user = next((u for u in self.users if u.email == email and u.is_active), None)
        if not user:
            return None
        
        reset_token = self.generate_reset_token()
        user.reset_token = reset_token
        user.reset_token_expiry = (datetime.datetime.now() + 
                                 datetime.timedelta(hours=24)).isoformat()
        self._save_users()
        return reset_token
    
    def reset_password(self, token: str, new_password: str) -> bool:
        user = next((u for u in self.users if hasattr(u, 'reset_token') and 
                    u.reset_token == token and u.is_active), None)
        
        if not user:
            return False
        
        if hasattr(user, 'reset_token_expiry') and user.reset_token_expiry:
            try:
                expiry_time = datetime.datetime.fromisoformat(user.reset_token_expiry)
                if datetime.datetime.now() > expiry_time:
                    return False
            except ValueError:
                return False
        
        user.password_hash = user._hash_password(new_password)
        user.reset_token = None
        user.reset_token_expiry = None
        self._save_users()
        return True
    
    def validate_reset_token(self, token: str) -> bool:
        user = next((u for u in self.users if hasattr(u, 'reset_token') and 
                    u.reset_token == token and u.is_active), None)
        
        if not user:
            return False
        
        if hasattr(user, 'reset_token_expiry') and user.reset_token_expiry:
            try:
                expiry_time = datetime.datetime.fromisoformat(user.reset_token_expiry)
                return datetime.datetime.now() <= expiry_time
            except ValueError:
                return False
        
        return False
    
    def logout(self):
        self.current_user = None
    
    def add_contact(self, first_name: str, last_name: str, phone: str, **kwargs) -> bool:
        if not self.current_user:
            return False
        
        new_contact = Contact(self.next_contact_id, self.current_user.user_id, 
                             first_name, last_name, phone, **kwargs)
        self.contacts.append(new_contact)
        self.next_contact_id += 1
        self._save_contacts()
        return True
    
    def edit_contact(self, contact_id: int, **kwargs) -> bool:
        contact = self.get_contact_by_id(contact_id)
        if contact and contact.user_id == self.current_user.user_id:
            contact.update_contact(**kwargs)
            self._save_contacts()
            return True
        return False
    
    def delete_contact(self, contact_id: int) -> bool:
        contact = self.get_contact_by_id(contact_id)
        if contact and contact.user_id == self.current_user.user_id:
            self.contacts.remove(contact)
            self._save_contacts()
            return True
        return False
    
    def get_contact_by_id(self, contact_id: int) -> Optional[Contact]:
        for contact in self.contacts:
            if contact.contact_id == contact_id:
                return contact
        return None

    def get_user_contact_by_id(self, contact_id: int) -> Optional[Contact]:
        """
        Get a contact by ID, only if it belongs to the current user.
        """
        if not self.current_user:
            return None
        
        for contact in self.contacts:
            if contact.contact_id == contact_id and contact.user_id == self.current_user.user_id:
                return contact
        return None

    def toggle_favorite_contact(self, contact_id: int) -> Optional[bool]:
        """
        Toggle the is_favorite status of a contact.
        Returns True if contact is now favorite, False if not, and None if contact not found or not owned by user.
        """
        if not self.current_user:
            return None

        contact = self.get_user_contact_by_id(contact_id)
        
        if contact:
            if contact.is_favorite:
                contact.unmark_favorite()
                result = False
            else:
                contact.mark_as_favorite()
                result = True
            self._save_contacts()
            return result
        return None
    
    def search_contacts(self, keyword: str) -> List[Contact]:
        if not self.current_user:
            return []
        
        results = []
        keyword_lower = keyword.lower()
        for contact in self.contacts:
            if contact.user_id == self.current_user.user_id and not contact.is_blocked:
                search_fields = [
                    contact.first_name, contact.last_name, contact.phone,
                    contact.email, contact.address, contact.group, contact.notes
                ]
                if any(keyword_lower in str(field).lower() for field in search_fields):
                    results.append(contact)
        return results
    
    def get_contacts_by_group(self, group: str) -> List[Contact]:
        if not self.current_user:
            return []
        
        return [contact for contact in self.contacts 
                if contact.user_id == self.current_user.user_id 
                and contact.group == group 
                and not contact.is_blocked]
    
    def get_favorite_contacts(self) -> List[Contact]:
        if not self.current_user:
            return []
        
        return [contact for contact in self.contacts 
                if contact.user_id == self.current_user.user_id 
                and contact.is_favorite 
                and not contact.is_blocked]
    
    
    
    def export_contacts_to_txt(self, filename: str) -> bool:
        if not self.current_user:
            return False
        
        user_contacts = [contact for contact in self.contacts 
                        if contact.user_id == self.current_user.user_id 
                        and not contact.is_blocked]
        
        if not user_contacts:
            return False
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                # Ghi tiêu đề
                header = "first_name,last_name,phone,email,address,group,notes"
                f.write(header + '\n')
                
                # Ghi dữ liệu từng liên hệ
                for contact in user_contacts:
                    line = ",".join([
                        contact.first_name,
                        contact.last_name,
                        contact.phone,
                        contact.email,
                        contact.address,
                        contact.group,
                        contact.notes.replace('\n', ' ') 
                    ])
                    f.write(line + '\n')
            return True
        except Exception as e:
            print(f"Export error: {e}")
            return False
    
    def import_contacts_from_txt(self, filename: str) -> Dict[str, int]:
        if not self.current_user:
            return {"success": 0, "failed": 0, "total": 0}
        
        results = {"success": 0, "failed": 0, "total": 0}
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if not lines:
                    return results
                
                # Giả định dòng đầu tiên là tiêu đề (header)
                header = [h.strip() for h in lines[0].strip().split(',')]
                
                for line in lines[1:]: # Bỏ qua dòng tiêu đề
                    line = line.strip()
                    if not line:
                        continue
                        
                    results["total"] += 1
                    try:
                        # Tách các trường dữ liệu dựa trên dấu phẩy (,)
                        values = [v.strip() for v in line.split(',')]
                        
                        # Tạo một dictionary từ header và values
                        if len(header) != len(values):
                            raise ValueError("Mismatched number of fields in line.")
                        
                        row = dict(zip(header, values))
                        
                        phone = row.get('phone')
                        if not phone:
                            results["failed"] += 1
                            continue
                        
                        # Thêm liên hệ
                        self.add_contact(
                            first_name=row.get('first_name', ''),
                            last_name=row.get('last_name', ''),
                            phone=phone,
                            email=row.get('email', ''),
                            address=row.get('address', ''),
                            group=row.get('group', 'General'),
                            notes=row.get('notes', '')
                        )
                        results["success"] += 1
                    except Exception as e:
                        print(f"Import line failed: {e}")
                        results["failed"] += 1
        except Exception as e:
            print(f"Import error: {e}")
        
        return results
    
    def backup_data(self) -> str:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(self.backups_dir, f"backup_{timestamp}.txt")
        
        backup_lines = [f"--- PhoneBook System Backup: {timestamp} ---"]
        
        # Sao lưu Users
        backup_lines.append("\n### USERS ###")
        for user in self.users:
            user_data = user.to_dict()
            backup_lines.append(f"User ID: {user_data['user_id']}")
            backup_lines.append(f"  Username: {user_data['username']}")
            backup_lines.append(f"  Email: {user_data['email']}")
            backup_lines.append(f"  Role: {user_data['role']}")
            backup_lines.append(f"  Is Active: {user_data['is_active']}")
            # Không nên sao lưu password_hash vào plain text
            backup_lines.append("  (Password hash omitted)")
            backup_lines.append("-" * 20)
            
        # Sao lưu Contacts
        backup_lines.append("\n### CONTACTS ###")
        for contact in self.contacts:
            contact_data = contact.to_dict()
            backup_lines.append(f"Contact ID: {contact_data['contact_id']} | User ID: {contact_data['user_id']}")
            backup_lines.append(f"  Name: {contact_data['first_name']} {contact_data['last_name']}")
            backup_lines.append(f"  Phone: {contact_data['phone']}")
            backup_lines.append(f"  Email: {contact_data.get('email', 'N/A')}")
            backup_lines.append(f"  Group: {contact_data.get('group', 'N/A')}")
            backup_lines.append(f"  Notes: {contact_data.get('notes', 'N/A')[:50]}...")
            backup_lines.append("=" * 30)

        # Ghi nội dung vào file .txt
        try:
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(backup_lines))
            return backup_file
        except Exception as e:
            print(f"Error during backup: {e}")
            return f"Backup failed: {e}"
    
    def get_all_users(self) -> List[User]:
        if not self.current_user or self.current_user.role != "admin":
            return []
        return self.users
    
    def deactivate_user(self, user_id: int) -> bool:
        if not self.current_user or self.current_user.role != "admin":
            return False
        
        for user in self.users:
            if user.user_id == user_id:
                user.is_active = False
                self._save_users()
                return True
        return False

    def activate_user(self, user_id: int) -> bool:
        if not self.current_user or self.current_user.role != "admin":
            return False
        
        for user in self.users:
            if user.user_id == user_id:
                user.is_active = True
                self._save_users()
                return True
        return False