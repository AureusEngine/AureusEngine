
def generate_shaping_curve(dev_signature):
    """
    Generates a normalized shaping distribution from a 3-material deviation signature.
    Returns a 6-tier probability distribution aligned to P→Y (indices 0–5).
    """
    min_dev, mid_dev, max_dev = sorted(dev_signature)

    # Define influence: strongest skew from min, weaker from max
    weights = [1.0, 0.5, 0.3]
    tier_bins = [0.0] * 6

    for i, dev in enumerate([min_dev, mid_dev, max_dev]):
        for t in range(6):
            delta = abs(t - dev)
            contrib = max(0, 1.0 - (delta / 6.0)) * weights[i]
            tier_bins[t] += contrib

    total = sum(tier_bins)
    return [round((x / total) * 100, 2) for x in tier_bins]
