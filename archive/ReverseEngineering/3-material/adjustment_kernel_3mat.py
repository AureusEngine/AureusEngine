
def apply_adjustment(profile, min_tier, max_tier):
    """
    Applies post-shaping adjustment and clamps output strictly to [min, max].
    """
    clamped = [0.0 if i < min_tier or i > max_tier else v for i, v in enumerate(profile)]
    total = sum(clamped)
    return [round((x / total) * 100, 2) if total else 0.0 for x in clamped]
