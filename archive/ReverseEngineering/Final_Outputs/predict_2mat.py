
from typing import List, Tuple, Dict

# Canonical deviation profiles for (0, d) where d = 0 through 5
CANONICAL_PROFILES: Dict[Tuple[int, int], List[float]] = {
    (0, 0): [100.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    (0, 1): [60.0, 40.0, 0.0, 0.0, 0.0, 0.0],
    (0, 2): [57.14, 14.29, 28.57, 0.0, 0.0, 0.0],
    (0, 3): [50.0, 20.0, 10.0, 20.0, 0.0, 0.0],
    (0, 4): [42.86, 21.43, 14.29, 7.14, 14.29, 0.0],
    (0, 5): [36.84, 21.05, 15.79, 10.53, 5.26, 10.53],
}

# Tier mapping
TIER_MAP: Dict[str, int] = {
    "P": 0,
    "C": 1,
    "F": 2,
    "X": 3,
    "E": 4,
    "Y": 5
}

TIER_LABELS: List[str] = ["P", "C", "F", "X", "E", "Y"]

def predict_2mat_distribution(mat1: str, mat2: str) -> Dict[str, float]:
    """
    Compute the canonical 2-material output distribution from two material tier labels.

    Args:
        mat1: First material tier label (e.g., "P", "C", "X")
        mat2: Second material tier label

    Returns:
        Dictionary mapping quality tier labels to output percentages (rounded to 2 decimals)
    """
    # Convert to tier indices
    t1, t2 = TIER_MAP[mat1], TIER_MAP[mat2]
    low, high = sorted([t1, t2])
    deviation = high - low
    profile = CANONICAL_PROFILES.get((0, deviation))

    if profile is None:
        raise ValueError(f"Unsupported deviation level: {deviation}")

    # Shift profile up to match the actual tier window
    shifted = [0.0] * 6
    for i, val in enumerate(profile):
        if i + low < 6:
            shifted[i + low] = round(val, 2)

    return dict(zip(TIER_LABELS, shifted))
