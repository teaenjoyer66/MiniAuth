from api_client import login, check_session
import tkinter as tk
from ui_login import LoginApp

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()