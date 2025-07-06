# Handles pattern matching, inversion, and rotation for crafted result sequences

def rotate_pattern(pattern, offset):
    return pattern[offset:] + pattern[:offset]

def invert_pattern(pattern):
    inversion = {'W': 'L', 'L': 'W'}
    return ''.join(inversion.get(char, char) for char in pattern)

def generate_pattern_variants(pattern):
    variants = set()
    variants.add(pattern)
    variants.add(invert_pattern(pattern))
    for i in range(1, len(pattern)):
        variants.add(rotate_pattern(pattern, i))
        variants.add(invert_pattern(rotate_pattern(pattern, i)))
    return variants