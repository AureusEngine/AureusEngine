# Uses real crafting outcomes to update pattern reliability and learning

from collections import defaultdict

class FeedbackManager:
    def __init__(self):
        self.correct_predictions = defaultdict(int)
        self.total_predictions = defaultdict(int)

    def update_feedback(self, pattern_id, correct):
        self.total_predictions[pattern_id] += 1
        if correct:
            self.correct_predictions[pattern_id] += 1

    def get_accuracy(self, pattern_id):
        total = self.total_predictions[pattern_id]
        if total == 0:
            return 0.0
        return self.correct_predictions[pattern_id] / total