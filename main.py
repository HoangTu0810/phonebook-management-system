from system import PhoneBookSystem
from ui import PhoneBookUI

def main():
    """Main function to start the application"""
    try:
        # Create default admin user if not exists
        system = PhoneBookSystem()
        if not any(user.role == "admin" for user in system.users):
            success = system.register_user("admin", "admmin@system.com", "admin123", "admin")
            if success:
                print("Default admin account created:")
                print("Email: admin@system.com")
                print("Password: admin123")
                print("Please change password after login!")
            else:
                print("Could not create default admin account!")
            input("Press Enter to continue...")
        
        # Start user interface
        ui = PhoneBookUI()
        ui.main_menu()
        print("Thank you for using the system!")
    except Exception as e:
        print(f"Application startup error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()