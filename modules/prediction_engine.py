def predict_next_outcome(session_data, pattern_model, material_distribution, gear_type):
    if not session_data:
        return "P", 0.0
    pattern = max(pattern_model.items(), key=lambda x: x[1]["confidence"], default=(None, None))
    if pattern[0] is None:
        return "P", 0.0
    return pattern[1]["next"], pattern[1]["confidence"]