# auth.py

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

class AuthService:
    def __init__(self):
        # Default users
        self.users = {
            "admin": User("admin", "admin123", "Admin"),
            "user": User("user", "user123", "User")
        }

    def authenticate(self, username, password):
        user = self.users.get(username)
        if user and user.password == password:
            print(f"Welcome, {username}!")
            return user
        else:
            print("Invalid username or password.")
            return None
