
# confidence_engine.py

STABLE_CONFIDENCE_THRESHOLD = 0.85
PATTERN_STABILITY_WINDOW = 10
PATTERN_DECAY_RATE = 0.95
PATTERN_MAX_AGE = 200

def adjust_confidence_for_length(base_confidence, pattern_length):
    if pattern_length <= 5:
        multiplier = 2.0 if pattern_length == 4 else 1.25
        return base_confidence * multiplier
    return base_confidence

def decay_confidence(confidence, age):
    return confidence * (PATTERN_DECAY_RATE ** age)
