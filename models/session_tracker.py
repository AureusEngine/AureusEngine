
class SessionTracker:
    def __init__(self):
        self.current_session = []
        self.all_sessions = []

    def add_result(self, result):
        self.current_session.append(result)

    def end_session(self):
        if self.current_session:
            self.all_sessions.append(self.current_session.copy())
            self.current_session.clear()

    def get_recent_session(self):
        return self.all_sessions[-1] if self.all_sessions else []

    def get_all_sessions(self):
        return self.all_sessions
