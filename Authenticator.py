# Authenticator.py

import tkinter as tk
from firebase_admin import credentials, auth, initialize_app

class Authenticator:
    def __init__(self, window, email_entry, password_entry, password_requirement_label, on_authentication_success):
        self.window = window
        self.email_entry = email_entry
        self.password_entry = password_entry
        self.password_requirement_label = password_requirement_label
        self.on_authentication_success = on_authentication_success

        self.initialize_firebase()

    def initialize_firebase(self):
        cred = credentials.Certificate('programmingproject-6feb8-firebase-adminsdk-mr5m7-c39ec49a74.json')
        initialize_app(cred)

    def signup(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if len(password) < 6:
            self.password_requirement_label.config(text="Password must be at least 6 characters long.", fg="red")
            return

        try:
            user = auth.create_user(
                email=email,
                password=password
            )
            print(f"Successfully created user: {user.uid}")
            self.window.destroy()
            self.on_authentication_success()  # Invoke the callback function

            # ... (unchanged)

        except auth.EmailAlreadyExistsError:
            self.password_requirement_label.config(text="Email already exists.", fg="red")
        except ValueError as e:
            self.password_requirement_label.config(text=str(e), fg="red")
        except auth.FirebaseAuthError as e:
            error_message = str(e)
            if 'email' in error_message:
                self.password_requirement_label.config(text="Invalid email address.", fg="red")
            elif 'password' in error_message:
                self.password_requirement_label.config(text="Invalid password.", fg="red")
            else:
                self.password_requirement_label.config(text=error_message, fg="red")

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        try:
            user = auth.get_user_by_email(email)
            if user.email_verified:
                print(f"Successfully logged in: {user.uid}")
                self.window.destroy()
                success_window = tk.Tk()
                success_window.title("Success")
                success_window.minsize(600, 300)  # Set minimum size
                success_label = tk.Label(success_window, text="Login successful!", fg="green")
                success_label.pack()
                success_window.mainloop()
            else:
                self.password_requirement_label.config(text="Email not verified.", fg="red")
        except auth.UserNotFoundError:
            self.password_requirement_label.config(text="User not found.", fg="red")
        except auth.InvalidPasswordError:
            self.password_requirement_label.config(text="Invalid password.", fg="red")
        except auth.FirebaseAuthError as e:
            self.password_requirement_label.config(text=str(e), fg="red")
