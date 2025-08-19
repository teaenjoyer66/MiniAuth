import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
from session_manager import SessionManager
from process_control import ProcessMonitor
from typing import List, Dict
from logger import Logger

class SessionApp:
    def __init__(self, master: tk.Tk, session_data: Dict, login_window):
        self.master = master
        self.login_window = login_window
        self.master.title("MiniAuth - Active Session")
        self.logger = Logger()
        
        self.session_manager = SessionManager(session_data["session_start"], session_data["session_end"])
        self.allowed_apps: List[str] = session_data["allowed_apps"]
        self.launched_processes: List[subprocess.Popen] = []
        self.timer_id = None
        self.master.protocol("WM_DELETE_WINDOW", self._on_close)

        self.logger.log_event("session_started", f"Session started with allowed apps: {self.allowed_apps}")
        self.logger.log_event("session_start_time", f"Session start time: {session_data['session_start']}")  
        
        self._build_session_ui()
        
        self.process_monitor = ProcessMonitor(self.launched_processes, self.session_manager)
        monitor_thread = threading.Thread(target=self.process_monitor.run, daemon=True)
        monitor_thread.start()

    def _build_session_ui(self):
        main_frame = tk.Frame(self.master, padx=10, pady=10)
        main_frame.pack(expand=True, fill='both')

        self.timer_label = tk.Label(main_frame, text="Time remaining: --:--:--", font=("Helvetica", 16))
        self.timer_label.pack(pady=10)
        
        apps_frame = tk.Frame(main_frame)
        apps_frame.pack()
        
        for app_name in self.allowed_apps:
            app_frame = tk.Frame(apps_frame)
            app_frame.pack(fill='x', padx=5, pady=2)
            
            tk.Label(app_frame, text=app_name, width=20, anchor='w').pack(side='left')
            tk.Button(app_frame, text="Launch", command=lambda app=app_name: self._launch_app(app)).pack(side='right')

        logout_button = tk.Button(main_frame, text="Logout", command=self._on_logout)
        logout_button.pack(pady=20)

        self._update_timer()

    def _launch_app(self, executable: str):
        try:
            process = subprocess.Popen(executable)
            self.launched_processes.append(process)
            self.logger.log_event("app_launched",f"app launched: {executable}")
        except FileNotFoundError:
            messagebox.showerror("Error", f"Executable not found: {executable}")

    def _update_timer(self):
        remaining_time = self.session_manager.get_remaining_time()
        
        if remaining_time <= 0:
            self._stop_timer()
            self.logger.log_event("session_expired", "Session time has expired.")
            messagebox.showinfo("Session End", "Your time has expired! Applications will be closed.")
            self.master.destroy()
            return
            
        hours, rem = divmod(remaining_time, 3600)
        minutes, seconds = divmod(rem, 60)
        self.timer_label.config(text=f"Time remaining: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")
        self.timer_id = self.master.after(1000, self._update_timer)

    def _stop_timer(self):
        if self.timer_id:
            self.master.after_cancel(self.timer_id)

    def _on_logout(self):
        self.logger.log_event("logout", "User logged out.")
        self.logger.log_event("session_ended", "Session ended by user logout.") 
        self._stop_timer()
        self.master.destroy()
        self.login_window.master.deiconify()
        self.login_window._clear_entries()
    
    def _on_close(self):
        self.logger.log_event("session_closed", "Session window closed by user.")
        self._stop_timer()
        self.master.destroy()