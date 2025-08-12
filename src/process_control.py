import psutil
import time
import subprocess
from session_manager import SessionManager
from typing import List

class ProcessMonitor:
    def __init__(self, launched_processes: List[subprocess.Popen], session_manager: SessionManager):
        self.launched_processes = launched_processes
        self.session_manager = session_manager

    def run(self):
        while True:
            if not self.session_manager.is_session_active():
                self.close_all_launched_apps()
                break
            
            self.clean_up_closed_processes()
            time.sleep(1)

    def clean_up_closed_processes(self):
            self.launched_processes = [
            proc for proc in self.launched_processes if proc.poll() is None
        ]

    def close_all_launched_apps(self):
        for proc in self.launched_processes:
            if proc.poll() is None:
                try:
                    proc.kill()
                    print(f"Closing the application after the session ends:{proc.pid}")
                except psutil.NoSuchProcess:
                    continue