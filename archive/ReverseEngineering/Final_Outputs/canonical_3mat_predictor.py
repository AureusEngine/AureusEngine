
# canonical_3mat_predictor.py

tier_map = {"P": 0, "C": 1, "F": 2, "X": 3, "E": 4, "Y": 5}
reverse_map = {v: k for k, v in tier_map.items()}

# Canonical deviation signature map (truncated here for brevity)
canonical_3mat_map = {
    (0, 0, 1): [0.0, 0.0, 0.0, 42.86, 57.14, 0.0],
    (0, 1, 1): [0.0, 0.0, 0.0, 42.86, 57.14, 0.0],
    (0, 1, 2): [41.67, 16.67, 25.0, 16.67, 0.0, 0.0],
    (0, 2, 3): [41.67, 16.67, 25.0, 16.67, 0.0, 0.0],
    (0, 1, 4): [50.0, 18.75, 12.5, 6.25, 12.5, 0.0],
    (0, 2, 4): [0.0, 0.0, 44.44, 33.33, 22.22, 0.0],
    (0, 2, 5): [0.0, 0.0, 41.67, 16.67, 8.33, 33.33],
    (0, 3, 5): [0.0, 0.0, 41.67, 16.67, 8.33, 33.33],
    # Add all verified (0,x,y) signatures as needed
}

def predict_3mat_canonical_direct(materials):
    tiers = [tier_map[m] for m in materials]
    base = min(tiers)
    deviations = sorted([t - base for t in tiers])
    signature = tuple(deviations)

    profile = canonical_3mat_map.get(signature)
    if not profile:
        return {"error": f"Signature {signature} not found."}

    bins = [0.0] * 6
    for i, val in enumerate(profile):
        if i + base < 6:
            bins[i + base] += val

    total = sum(bins)
    final = [round((x / total) * 100, 2) for x in bins]
    return {reverse_map[i]: final[i] for i in range(6)}
