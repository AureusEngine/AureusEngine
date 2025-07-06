# confidence_model.py

def calculate_confidence(predicted, actual, history_length):
    '''
    Compute confidence score based on match frequency and history length.
    '''
    if history_length < 4:
        return 0.3  # low confidence due to small sample
    elif predicted == actual:
        return min(1.0, 0.5 + 0.05 * history_length)
    else:
        return max(0.0, 0.5 - 0.05 * history_length)