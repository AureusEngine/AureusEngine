# prediction_engine.py

def predict_next_outcome(session_data, pattern_model, material_distribution, gear_type):
    '''
    Analyze the current session's data and pattern model to predict the next outcome.
    '''
    if not session_data:
        return "P", 0.0

    # Example logic for high-confidence pattern retrieval
    pattern = max(pattern_model.items(), key=lambda x: x[1]["confidence"], default=(None, None))
    if pattern[0] is None:
        return "P", 0.0

    prediction = pattern[1]["next"]
    confidence = pattern[1]["confidence"]
    return prediction, confidence