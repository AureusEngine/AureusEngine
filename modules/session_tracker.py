from collections import defaultdict

class SessionTracker:
    def __init__(self):
        self.current_user = "default"
        self.sessions = defaultdict(list)             # Current active session
        self.archived_sessions = defaultdict(list)    # List of past sessions per user

    def switch_user(self, user_id):
        self.current_user = user_id
        # Initialize if new user
        if user_id not in self.sessions:
            self.sessions[user_id] = []
        if user_id not in self.archived_sessions:
            self.archived_sessions[user_id] = []

    def add_result(self, result):
        self.sessions[self.current_user].append(result)

    def last_result(self):
        if self.sessions[self.current_user]:
            return self.sessions[self.current_user][-1]
        return None

    def session_length(self):
        return len(self.sessions[self.current_user])

    def get_session_results(self):
        return self.sessions[self.current_user]

    def reset_session(self):
        self.sessions[self.current_user] = []

    def end_session(self):
        """Archives the current session and resets it."""
        if self.sessions[self.current_user]:
            self.archived_sessions[self.current_user].append(
                self.sessions[self.current_user].copy()
            )
            self.sessions[self.current_user].clear()

    def get_recent_session(self):
        if self.archived_sessions[self.current_user]:
            return self.archived_sessions[self.current_user][-1]
        return []

    def get_all_sessions(self):
        return self.archived_sessions[self.current_user]
