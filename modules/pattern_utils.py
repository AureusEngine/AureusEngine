# pattern_utils.py

def invert_pattern(pattern):
    return ["W" if p == "L" else "L" if p == "W" else p for p in pattern]

def rotate_pattern(pattern, positions=1):
    return pattern[positions:] + pattern[:positions]

def find_shape_matches(candidate, pattern_list):
    shape = "".join("W" if x == "W" else "L" if x == "L" else "M" for x in candidate)
    matches = []
    for pattern in pattern_list:
        target_shape = "".join("W" if x == "W" else "L" if x == "L" else "M" for x in pattern)
        if shape == target_shape:
            matches.append(pattern)
    return matches