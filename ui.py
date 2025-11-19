import os
from system import PhoneBookSystem

class PhoneBookUI:
    def __init__(self):
        self.system = PhoneBookSystem()
        self.running = True
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_header(self, title: str):
        print("=" * 50)
        print(f"{title:^50}")
        print("=" * 50)
    
    def wait_for_enter(self):
        input("\nPress Enter to continue...")
    
    def main_menu(self):
        while self.running:
            self.clear_screen()
            self.display_header("PHONEBOOK MANAGEMENT SYSTEM")
            
            if not self.system.current_user:
                print("1. Login")
                print("2. Register")
                print("3. Forgot Password")
                print("4. Exit")
            else:
                user_role = "Admin" if self.system.current_user.role == "admin" else "User"
                print(f"Welcome: {self.system.current_user.username} ({user_role})")
                print("\nMAIN MENU:")
                print("1. Contact Management")
                print("2. Search Contacts")
                print("3. Favorite Contacts")
                print("4. Import/Export")
                if self.system.current_user.role == "admin":
                    print("5. User Management (Admin)")
                    print("6. System Backup (Admin)")
                print("7. Update Profile")
                print("8. Logout")
                print("9. Exit")
            
            choice = input("\nSelect function: ").strip()
            
            if not self.system.current_user:
                if choice == "1":
                    self.login()
                elif choice == "2":
                    self.register()
                elif choice == "3":
                    self.forgot_password()
                elif choice == "4":
                    self.running = False
                else:
                    print("Invalid choice!")
                    self.wait_for_enter()
            else:
                if choice == "1":
                    self.contact_management()
                elif choice == "2":
                    self.search_contacts()
                elif choice == "3":
                    self.favorite_contacts()
                elif choice == "4":
                    self.import_export_menu()
                elif choice == "5" and self.system.current_user.role == "admin":
                    self.user_management()
                elif choice == "6" and self.system.current_user.role == "admin":
                    self.system_backup()
                elif choice == "7":
                    self.update_profile()
                elif choice == "8":
                    self.system.logout()
                    print("Logged out successfully!")
                    self.wait_for_enter()
                elif choice == "9":
                    self.running = False
                else:
                    print("Invalid choice!")
                    self.wait_for_enter()
    
    def login(self):
        self.clear_screen()
        self.display_header("LOGIN")
        
        email = input("Email: ").strip()
        password = input("Password: ").strip()
        
        if self.system.login(email, password):
            print("Login successful!")
        else:
            print("Email or password incorrect!")
        
        self.wait_for_enter()
    
    def register(self):
        self.clear_screen()
        self.display_header("REGISTER")
        
        username = input("Username: ").strip()
        email = input("Email: ").strip()
        password = input("Password: ").strip()
        confirm_password = input("Confirm Password: ").strip()
        
        if password != confirm_password:
            print("Password confirmation does not match!")
            self.wait_for_enter()
            return
        
        if len(password) < 6:
            print("Password must be at least 6 characters!")
            self.wait_for_enter()
            return
        
        if self.system.register_user(username, email, password):
            print("Registration successful! Please login.")
        else:
            print("Email already exists in system!")
        
        self.wait_for_enter()
    
    def forgot_password(self):
        self.clear_screen()
        self.display_header("FORGOT PASSWORD")
        
        print("1. Request Password Reset")
        print("2. Reset Password with Token")
        print("3. Back")
        
        choice = input("\nSelect function: ").strip()
        
        if choice == "1":
            self.request_password_reset()
        elif choice == "2":
            self.reset_password_with_token()
        elif choice == "3":
            return
        else:
            print("Invalid choice!")
            self.wait_for_enter()
    
    def request_password_reset(self):
        self.clear_screen()
        self.display_header("REQUEST PASSWORD RESET")
        
        email = input("Enter registered email: ").strip()
        
        token = self.system.request_password_reset(email)
        if token:
            print(f"Password reset request successful!")
            print(f"Reset Token: {token}")
            print("Note: Token is valid for 24 hours")
            print("\nUse this token in 'Reset Password with Token' section")
        else:
            print("Email does not exist or account is deactivated!")
        
        self.wait_for_enter()
    
    def reset_password_with_token(self):
        self.clear_screen()
        self.display_header("RESET PASSWORD")
        
        token = input("Enter reset token: ").strip()
        
        if not self.system.validate_reset_token(token):
            print("Invalid or expired token!")
            self.wait_for_enter()
            return
        
        new_password = input("New Password: ").strip()
        confirm_password = input("Confirm Password: ").strip()
        
        if new_password != confirm_password:
            print("Password confirmation does not match!")
            self.wait_for_enter()
            return
        
        if len(new_password) < 6:
            print("Password must be at least 6 characters!")
            self.wait_for_enter()
            return
        
        if self.system.reset_password(token, new_password):
            print("Password reset successful! Please login again.")
        else:
            print("Error resetting password!")
        
        self.wait_for_enter()
    
    def contact_management(self):
        while True:
            self.clear_screen()
            self.display_header("CONTACT MANAGEMENT")
            
            # Liệt kê danh bạ (dùng hàm view_contacts nhưng không chờ Enter)
            user_contacts = [contact for contact in self.system.contacts 
                            if contact.user_id == self.system.current_user.user_id 
                            and not contact.is_blocked]
            
            if user_contacts:
                print("Your Contacts:")
                user_contacts.sort(key=lambda x: (x.first_name.lower(), x.last_name.lower()))
                for i, contact in enumerate(user_contacts, 1):
                    favorite = "*" if contact.is_favorite else " "
                    print(f"  ID:{contact.contact_id} | {favorite} {contact.first_name} {contact.last_name} - {contact.phone}")
                print("-" * 50)
            else:
                print("No contacts yet.")
                print("-" * 50)
                
            print("\nOPTIONS:")
            print("1. Add New Contact")
            print("2. Edit Contact")
            print("3. Delete Contact")
            print("4. Toggle Favorite Status") # TÙY CHỌN MỚI
            print("5. Back to Main Menu") # ĐỔI SỐ THỨ TỰ
            
            choice = input("\nSelect function: ").strip()
            
            if choice == "1":
                self.add_contact()
            elif choice == "2":
                self.edit_contact()
            elif choice == "3":
                self.delete_contact()
            elif choice == "4": # CHỨC NĂNG MỚI
                self.toggle_favorite_ui()
            elif choice == "5":
                break
            else:
                print("Invalid choice!")
                self.wait_for_enter()

    def toggle_favorite_ui(self):
        self.clear_screen()
        self.display_header("TOGGLE FAVORITE STATUS")

        contact_id_str = input("Enter Contact ID to toggle favorite status: ").strip()
        if not contact_id_str.isdigit():
            print("Invalid Contact ID. Must be a number.")
            self.wait_for_enter()
            return

        contact_id = int(contact_id_str)

        result = self.system.toggle_favorite_contact(contact_id)

        if result is True:
            print(f"Success: Contact with ID {contact_id} is now marked as **Favorite**.")
        elif result is False:
            print(f"Success: Contact with ID {contact_id} is now **NOT** a favorite.")
        elif result is None:
            print(f"Error: Contact with ID {contact_id} not found or does not belong to you.")
        else:
            print("Error: Could not update favorite status.")

        self.wait_for_enter()

    def view_contacts(self):
        self.clear_screen()
        self.display_header("CONTACT LIST")
        
        user_contacts = [contact for contact in self.system.contacts 
                        if contact.user_id == self.system.current_user.user_id 
                        and not contact.is_blocked]
        
        if not user_contacts:
            print("No contacts yet.")
            self.wait_for_enter()
            return
        
        user_contacts.sort(key=lambda x: (x.first_name.lower(), x.last_name.lower()))
        
        for i, contact in enumerate(user_contacts, 1):
            favorite = "* " if contact.is_favorite else "  "
            print(f"{i}. [ID: {contact.contact_id}] {favorite}{contact.first_name} {contact.last_name} - {contact.phone}")
            print(f"   Email: {contact.email} | Group: {contact.group}")
            if contact.address:
                print(f"   Address: {contact.address}")
            if contact.notes:
                print(f"   Notes: {contact.notes}")
            print("-" * 50)
        
        self.wait_for_enter()
    
    def add_contact(self):
        self.clear_screen()
        self.display_header("ADD NEW CONTACT")
        
        first_name = input("First Name: ").strip()
        last_name = input("Last Name: ").strip()
        phone = input("Phone (*): ").strip()
        
        if not phone:
            print("Phone number is required!")
            self.wait_for_enter()
            return
        
        email = input("Email: ").strip()
        address = input("Address: ").strip()
        group = input("Group (General/Family/Friends/Work): ").strip() or "General"
        notes = input("Notes: ").strip()
        
        if self.system.add_contact(first_name, last_name, phone, 
                                 email=email, address=address, group=group, notes=notes):
            print("Contact added successfully!")
        else:
            print("Error adding contact!")
        
        self.wait_for_enter()
    
    def edit_contact(self):
        self.clear_screen()
        self.display_header("EDIT CONTACT")
        
        # Lấy ID của người dùng muốn chỉnh sửa, không dùng index nữa
        user_contacts = [contact for contact in self.system.contacts 
                        if contact.user_id == self.system.current_user.user_id 
                        and not contact.is_blocked]
        
        if not user_contacts:
            print("No contacts to edit.")
            self.wait_for_enter()
            return
        
        print("Available Contacts:")
        for contact in user_contacts:
            print(f"ID: {contact.contact_id}. {contact.first_name} {contact.last_name} - {contact.phone}")
        
        try:
            contact_id = int(input("\nEnter Contact ID to edit: ").strip())
            contact = self.system.get_user_contact_by_id(contact_id) # Dùng hàm mới để check quyền
            
            if contact:
                print(f"\nEditing contact: {contact.first_name} {contact.last_name}")
                print("(Leave blank to keep current value)")
                
                first_name = input(f"First Name [{contact.first_name}]: ").strip() or contact.first_name
                last_name = input(f"Last Name [{contact.last_name}]: ").strip() or contact.last_name
                phone = input(f"Phone [{contact.phone}]: ").strip() or contact.phone
                email = input(f"Email [{contact.email}]: ").strip() or contact.email
                address = input(f"Address [{contact.address}]: ").strip() or contact.address
                group = input(f"Group [{contact.group}]: ").strip() or contact.group
                notes = input(f"Notes [{contact.notes}]: ").strip() or contact.notes
                
                updates = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'phone': phone,
                    'email': email,
                    'address': address,
                    'group': group,
                    'notes': notes
                }
                
                if self.system.edit_contact(contact.contact_id, **updates):
                    print("Contact updated successfully!")
                else:
                    print("Error updating contact!")
            else:
                print(f"Contact with ID {contact_id} not found or does not belong to you.")
        except ValueError:
            print("Please enter a valid number for Contact ID!")
        
        self.wait_for_enter()
    
    def delete_contact(self):
        self.clear_screen()
        self.display_header("DELETE CONTACT")
        
        user_contacts = [contact for contact in self.system.contacts 
                        if contact.user_id == self.system.current_user.user_id 
                        and not contact.is_blocked]
        
        if not user_contacts:
            print("No contacts to delete.")
            self.wait_for_enter()
            return
        
        print("Available Contacts:")
        for contact in user_contacts:
            print(f"ID: {contact.contact_id}. {contact.first_name} {contact.last_name} - {contact.phone}")
        
        try:
            contact_id = int(input("\nEnter Contact ID to delete: ").strip())
            contact = self.system.get_user_contact_by_id(contact_id)
            
            if contact:
                confirm = input(f"Are you sure you want to delete '{contact.first_name} {contact.last_name}' (ID: {contact.contact_id})? (y/n): ")
                if confirm.lower() == 'y':
                    if self.system.delete_contact(contact.contact_id):
                        print("Contact deleted successfully!")
                    else:
                        print("Error deleting contact!")
                else:
                    print("Delete operation cancelled.")
            else:
                print(f"Contact with ID {contact_id} not found or does not belong to you.")
        except ValueError:
            print("Please enter a valid number for Contact ID!")
        
        self.wait_for_enter()
    
    def search_contacts(self):
        self.clear_screen()
        self.display_header("SEARCH CONTACTS")
        
        keyword = input("Enter search keyword: ").strip()
        
        if not keyword:
            print("Please enter a search keyword!")
            self.wait_for_enter()
            return
        
        results = self.system.search_contacts(keyword)
        
        if not results:
            print("No contacts found matching your search.")
        else:
            print(f"Found {len(results)} results:")
            for i, contact in enumerate(results, 1):
                favorite = "* " if contact.is_favorite else "  "
                print(f"{i}. [ID: {contact.contact_id}] {favorite}{contact.first_name} {contact.last_name} - {contact.phone}")
                print(f"   Email: {contact.email} | Group: {contact.group}")
                print("-" * 50)
        
        self.wait_for_enter()
    
    def favorite_contacts(self):
        self.clear_screen()
        self.display_header("FAVORITE CONTACTS")
        
        favorites = self.system.get_favorite_contacts()
        
        if not favorites:
            print("No favorite contacts yet.")
            self.wait_for_enter()
            return
        
        for i, contact in enumerate(favorites, 1):
            print(f"{i}. [ID: {contact.contact_id}] * {contact.first_name} {contact.last_name} - {contact.phone}")
            print(f"   Email: {contact.email} | Group: {contact.group}")
            print("-" * 50)
        
        self.wait_for_enter()
    
    def import_export_menu(self):
        while True:
            self.clear_screen()
            self.display_header("IMPORT/EXPORT DATA")
            
            print("1. Export Contacts to TXT") # Đổi tên hiển thị
            print("2. Import Contacts from TXT") # Đổi tên hiển thị
            print("3. Back")
            
            choice = input("\nSelect function: ").strip()
            
            if choice == "1":
                filename = input("TXT filename to export: ").strip()
                if not filename.endswith('.txt'):
                    filename += '.txt'
                
                if self.system.export_contacts_to_txt(filename): # Gọi hàm mới
                    print(f"Data exported successfully to: {filename}")
                else:
                    print("Error exporting data!")
                self.wait_for_enter()
            
            elif choice == "2":
                filename = input("TXT filename to import: ").strip()
                if os.path.exists(filename):
                    results = self.system.import_contacts_from_txt(filename) # Gọi hàm mới
                    print(f"Import results:")
                    print(f"- Total records: {results['total']}")
                    print(f"- Successful: {results['success']}")
                    print(f"- Failed: {results['failed']}")
                else:
                    print("File does not exist!")
                self.wait_for_enter()
            
            elif choice == "3":
                break
            
            else:
                print("Invalid choice!")
                self.wait_for_enter()
    
    def user_management(self):
        if not self.system.current_user or self.system.current_user.role != "admin":
            print("Access denied!")
            self.wait_for_enter()
            return
        
        while True:
            self.clear_screen()
            self.display_header("USER MANAGEMENT (ADMIN)")
            
            users = self.system.get_all_users()
            
            print("User List:")
            for user in users:
                status = "Active" if user.is_active else "Inactive"
                print(f"{user.user_id}. {user.username} ({user.email}) - {user.role} [{status}]")
            
            print("\n1. Deactivate User")
            print("2. Activate User")
            print("3. Back")
            
            choice = input("\nSelect function: ").strip()
            
            if choice == "1":
                try:
                    user_id = int(input("Enter user ID to deactivate: "))
                    if self.system.deactivate_user(user_id):
                        print("User deactivated successfully!")
                    else:
                        print("Error deactivating user!")
                    self.wait_for_enter()
                except ValueError:
                    print("Invalid user ID!")
                    self.wait_for_enter()
            
            elif choice == "2":
                try:
                    user_id = int(input("Enter user ID to activate: "))
                    if self.system.activate_user(user_id):
                        print("User activated successfully!")
                    else:
                        print("Error activating user!")
                    self.wait_for_enter()
                except ValueError:
                    print("Invalid user ID!")
                    self.wait_for_enter()
            
            elif choice == "3":
                break
            
            else:
                print("Invalid choice!")
                self.wait_for_enter()
    
    def system_backup(self):
        if not self.system.current_user or self.system.current_user.role != "admin":
            print("Access denied!")
            self.wait_for_enter()
            return
        
        self.clear_screen()
        self.display_header("SYSTEM BACKUP")
        
        backup_file = self.system.backup_data()
        print(f"Data backup successful!")
        print(f"Backup file: {backup_file}")
        
        self.wait_for_enter()
    
    def update_profile(self):
        self.clear_screen()
        self.display_header("UPDATE PROFILE")
        
        user = self.system.current_user
        print(f"Current Information:")
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        
        print("\nEnter new information (leave blank to keep current):")
        new_username = input(f"New Username [{user.username}]: ").strip()
        new_email = input(f"New Email [{user.email}]: ").strip()
        
        updates = {}
        if new_username:
            updates['username'] = new_username
        if new_email:
            if new_email != user.email and any(u.email == new_email for u in self.system.users):
                print("Email already exists in system!")
                self.wait_for_enter()
                return
            updates['email'] = new_email
        
        if updates:
            user.update_profile(**updates)
            self.system._save_users()
            print("Profile updated successfully!")
        else:
            print("No changes made.")
        
        self.wait_for_enter()