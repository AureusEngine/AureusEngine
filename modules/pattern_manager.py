# pattern_manager.py

from collections import defaultdict
from .constants import MIN_PATTERN_LENGTH, MAX_PATTERN_LENGTH, PATTERN_DECAY_RATE, PATTERN_MAX_AGE
from modules.utils.firebase_utils import (
    retrieve_user_patterns,
    retrieve_engine_patterns,
    upload_engine_patterns,
    sanitize_pattern
)

class PatternManager:
    def __init__(self):
        self.pattern_store = defaultdict(lambda: {"count": 0, "last_seen": 0, "age": 0, "source": "engine"})
        self._load_user_patterns()
        self._load_engine_patterns()

    def _load_user_patterns(self):
        """Load sanitized user-submitted patterns from Firebase with lower confidence."""
        user_patterns = retrieve_user_patterns()
        for pattern_str in user_patterns:
            pattern = tuple(sanitize_pattern(pattern_str))
            self.pattern_store[pattern] = {
                "count": 0.5,
                "last_seen": -1,
                "age": 0,
                "source": "user"
            }

    def _load_engine_patterns(self):
        """Load internal (engine-detected) patterns from Firebase."""
        engine_data = retrieve_engine_patterns()
        for pattern_str, data in engine_data.items():
            pattern = tuple(sanitize_pattern(pattern_str))
            self.pattern_store[pattern] = {
                "count": float(data.get("count", 1)),
                "last_seen": int(data.get("last_seen", 0)),
                "age": int(data.get("age", 0)),
                "source": "engine"
            }

    def update_patterns(self, session_data):
        for length in range(MIN_PATTERN_LENGTH, min(MAX_PATTERN_LENGTH + 1, len(session_data))):
            for i in range(len(session_data) - length + 1):
                pattern = tuple(session_data[i:i + length])
                if pattern in self.pattern_store and self.pattern_store[pattern]["source"] == "user":
                    continue  # Don't overwrite user-submitted patterns
                self.pattern_store[pattern]["count"] += 1
                self.pattern_store[pattern]["last_seen"] = len(session_data)
                self.pattern_store[pattern]["age"] = 0
                self.pattern_store[pattern]["source"] = "engine"

        self.decay_patterns()
        self._save_engine_patterns()

    def decay_patterns(self):
        for pattern in list(self.pattern_store):
            if self.pattern_store[pattern]["source"] == "user":
                continue
            self.pattern_store[pattern]["age"] += 1
            self.pattern_store[pattern]["count"] *= PATTERN_DECAY_RATE
            if self.pattern_store[pattern]["age"] > PATTERN_MAX_AGE:
                del self.pattern_store[pattern]

    def _save_engine_patterns(self):
        """Upload engine-learned patterns to Firebase."""
        to_store = {}
        for pattern, data in self.pattern_store.items():
            if data["source"] == "engine":
                key = ''.join(pattern)  # Serialize tuple
                to_store[key] = {
                    "count": data["count"],
                    "last_seen": data["last_seen"],
                    "age": data["age"]
                }
        upload_engine_patterns(to_store)

    def get_common_patterns(self):
        sorted_patterns = sorted(self.pattern_store.items(), key=lambda x: -x[1]["count"])
        return [pat for pat, data in sorted_patterns if data["count"] > 1]
