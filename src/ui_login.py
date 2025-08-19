import tkinter as tk
from tkinter import messagebox
from api_client import login
from ui_session import SessionApp
from logger import Logger 

class LoginApp:
    def __init__(self, master: tk.Tk):
        self.master = master
        self.master.title("MiniAuth - Login")
        self.logger = Logger()
        self._build_login_ui()
    
    def _build_login_ui(self):
        frame = tk.Frame(self.master, padx=10, pady=10)
        frame.pack(expand=True, fill='both')

        tk.Label(frame, text="Email:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.email_entry = tk.Entry(frame, width=30)
        self.email_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.password_entry = tk.Entry(frame, width=30, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        login_button = tk.Button(frame, text="Login", command=self._on_login)
        login_button.grid(row=2, column=0, columnspan=2, pady=10)

    def _on_login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showwarning("Error", "Enter email and password.")
            return

        result = login(email, password)

        if "token" in result:
            self.logger.log_event('login_success',f"User {email} logged in successfully.")
            messagebox.showinfo("Success", "You have logged in successfully!")
            self.master.withdraw()
            
            session_data = {
                "session_start": result["session_start"],
                "session_end": result["session_end"],
                "allowed_apps": result["allowed_apps"],
            }
            
            session_root = tk.Tk()
            SessionApp(session_root, session_data, self)
            session_root.mainloop()
        else:
            error_msg = result.get("error", "Unknown login error.")
            self.logger.log_event('login_failed', f"Login failed for user {email}: {error_msg}")
            messagebox.showerror("Login error", error_msg)
            
    def _clear_entries(self):
        self.email_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')