def filter_invalid_patterns(patterns, gear_type, valid_lengths):
    return [
        p for p in patterns
        if len(p) in valid_lengths and (gear_type in p or gear_type == "All")
    ]

def age_and_decay_patterns(patterns, decay_rate=0.95, max_age=200):
    aged_patterns = {}
    for pattern, data in patterns.items():
        data['age'] += 1
        if data['age'] > max_age:
            continue
        data['confidence'] *= decay_rate
        aged_patterns[pattern] = data
    return aged_patterns