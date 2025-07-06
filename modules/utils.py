# utils.py

def normalize_pattern(pattern):
    return ''.join(pattern).upper().strip()

def alias_to_quality(input_alias):
    mapping = {'1': 'W', '2': 'L', '3': 'M'}
    return mapping.get(input_alias, input_alias)

def quality_to_score(quality, max_quality, min_quality):
    if quality == max_quality:
        return "W"
    elif quality == min_quality:
        return "L"
    else:
        return "M"