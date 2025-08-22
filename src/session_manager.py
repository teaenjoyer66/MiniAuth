from datetime import datetime
from typing import Optional

class SessionManager:
    def __init__(self, session_start_iso: Optional[str] = None, session_end_iso: Optional[str] = None):
        self.session_start_time: Optional[datetime] = None
        self.session_end_time: Optional[datetime] = None
        
        if session_start_iso and session_end_iso:
            self.session_start_time = datetime.fromisoformat(session_start_iso)
            self.session_end_time = datetime.fromisoformat(session_end_iso)
        
        self._forced_end = False
    
    def force_end_session(self):
        self._forced_end = True

    def is_session_active(self) -> bool:
        if self._forced_end:
            return False
        return self.get_remaining_time() > 0
    
    def get_remaining_time(self) -> float:
        if self.session_end_time is None:
            return 0.0
        
        remaining = (self.session_end_time - datetime.now()).total_seconds()
        return max(0.0, remaining)
