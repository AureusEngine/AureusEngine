
# pattern_tracking.py

from collections import defaultdict
import math

class PatternTracker:
    def __init__(self):
        self.patterns = defaultdict(lambda: {"count": 0, "confidence": 0.0, "last_seen": 0})

    def record_pattern(self, pattern, session_id, result):
        if pattern in self.patterns:
            self.patterns[pattern]["count"] += 1
            self.patterns[pattern]["last_seen"] = session_id
            self.patterns[pattern]["confidence"] = self._calculate_confidence(self.patterns[pattern]["count"])
        else:
            self.patterns[pattern] = {"count": 1, "confidence": 0.1, "last_seen": session_id}

    def _calculate_confidence(self, count):
        return min(1.0, math.log(count + 1) / math.log(10))

    def get_confident_patterns(self, threshold=0.75):
        return {p: d for p, d in self.patterns.items() if d["confidence"] >= threshold}
