
# m_tier_logic.py

QUALITY_SCORES = {"P": 1, "C": 2, "R": 3, "X": 4, "E": 5, "Y": 6}

def classify_result(materials, result_quality):
    values = sorted(QUALITY_SCORES[q] for q in materials)
    min_val, max_val = values[0], values[-1]
    result_score = QUALITY_SCORES[result_quality]

    if result_score == max_val:
        return "W"
    elif result_score == min_val and all(q == "P" for q in materials):
        return "W"
    elif result_score == min_val:
        return "L"
    else:
        mid_index = values.index(result_score) if result_score in values else -1
        return f"M{mid_index + 1}" if mid_index != -1 else "M?"
