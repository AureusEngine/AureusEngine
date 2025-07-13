class PatternDecay:
    def __init__(self, decay_rate=0.95, max_age=200):
        self.decay_rate = decay_rate
        self.max_age = max_age

    def apply_decay(self, patterns):
        for pattern, metadata in patterns.items():
            metadata['age'] += 1
            if metadata['age'] > self.max_age:
                metadata['active'] = False
            else:
                metadata['confidence'] *= self.decay_rate
        return patterns