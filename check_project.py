import os
import excel_manager

print("Running from:", os.path.dirname(os.path.abspath(__file__)))
print("excel_manager loaded from:", os.path.abspath(excel_manager.__file__))
print("validate_login available:", hasattr(excel_manager, "validate_login"))
print("register_user available:", hasattr(excel_manager, "register_user"))
print("username_exists available:", hasattr(excel_manager, "username_exists"))
