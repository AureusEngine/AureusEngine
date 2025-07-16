
# override_shaping_kernels.py

tier_map = {"P": 0, "C": 1, "F": 2, "X": 3, "E": 4, "Y": 5}
reverse_map = {v: k for k, v in tier_map.items()}

canonical_2mat_profiles = {
    (0, 1): [71.43, 28.57, 0.0, 0.0, 0.0, 0.0],
    (0, 2): [66.67, 11.11, 22.22, 0.0, 0.0, 0.0],
    (0, 3): [58.33, 16.67, 8.33, 16.67, 0.0, 0.0],
    (0, 4): [50.0, 18.75, 12.5, 6.25, 12.5, 0.0],
    (0, 5): [44.44, 16.67, 11.11, 5.56, 5.56, 16.67]
}

def shape_2mat(tier1: str, tier2: str) -> dict:
    t1 = tier_map[tier1]
    t2 = tier_map[tier2]

    if t1 == t2:
        bins = [0.0] * 6
        bins[t1] = 100.0
        return {reverse_map[i]: bins[i] for i in range(6)}

    d = abs(t2 - t1)
    low = min(t1, t2)
    base_profile = canonical_2mat_profiles.get((0, d), [0.0] * 6)

    bins = [0.0] * 6
    for i, val in enumerate(base_profile):
        if i + low < 6:
            bins[i + low] += val

    total = sum(bins)
    norm_bins = [round((x / total) * 100, 2) for x in bins]
    return {reverse_map[i]: norm_bins[i] for i in range(6)}

def shape_3mat_no_template(tier_a: str, tier_b: str, tier_c: str) -> dict:
    t = [tier_map[tier_a], tier_map[tier_b], tier_map[tier_c]]
    if t[0] == t[1] == t[2]:
        bins = [0.0] * 6
        bins[t[0]] = 100.0
        return {reverse_map[i]: bins[i] for i in range(6)}

    base = min(t)
    devs = [v - base for v in t]
    pairs = [(devs[i], devs[j]) for i in range(3) for j in range(i + 1, 3)]

    bins = [0.0] * 6
    for d1, d2 in pairs:
        low, high = sorted([d1, d2])
        diff = high - low
        base_profile = canonical_2mat_profiles.get((0, diff), [0.0] * 6)

        shifted = [0.0] * 6
        for i, val in enumerate(base_profile):
            if i + low + base < 6:
                shifted[i + low + base] += val
        bins = [bins[i] + shifted[i] for i in range(6)]

    total = sum(bins)
    norm_bins = [round((x / total) * 100, 2) for x in bins]
    return {reverse_map[i]: norm_bins[i] for i in range(6)}
