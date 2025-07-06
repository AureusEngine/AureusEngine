# pattern_engine.py
from collections import defaultdict, Counter
from .utils import normalize_pattern

class PatternEngine:
    def __init__(self):
        self.patterns = defaultdict(list)
        self.max_age = 200
        self.decay_rate = 0.95

    def record_outcome(self, pattern_key, outcome):
        self.patterns[pattern_key].append(outcome)
        if len(self.patterns[pattern_key]) > self.max_age:
            self.patterns[pattern_key] = self.patterns[pattern_key][-self.max_age:]

    def get_prediction(self, pattern_key):
        outcomes = self.patterns.get(pattern_key, [])
        if not outcomes:
            return None
        counter = Counter(outcomes)
        total = sum(counter.values())
        return {k: v / total for k, v in counter.items()}