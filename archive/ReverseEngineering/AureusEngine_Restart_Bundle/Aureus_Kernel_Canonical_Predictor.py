
import numpy as np
import math

tier_order = ["P", "C", "F", "X", "E", "Y"]
tier_index = {t: i for i, t in enumerate(tier_order)}
TEMPLATE_WEIGHT = 1.40
DECAY_T = 1.0  # Can be adjusted (e.g., 0.6)

def generate_kernel_arc(deviation: int, weight: float) -> np.ndarray:
    arc = np.zeros(6)
    for i in range(6):
        dist = abs(i - deviation)
        arc[i] = weight * math.exp(-DECAY_T * dist * dist)
    return arc

def predict_shaping_output(i1: str, i2: str, template: str) -> list:
    t1, t2, tt = tier_index[i1], tier_index[i2], tier_index[template]
    anchor = min(t1, t2, tt)
    max_tier = max(t1, t2, tt)

    d1, d2, dt = t1 - anchor, t2 - anchor, tt - anchor
    arc1 = generate_kernel_arc(d1, 1.0)
    arc2 = generate_kernel_arc(d2, 1.0)
    arc_t = generate_kernel_arc(dt, TEMPLATE_WEIGHT)

    combined = arc1 + arc2 + arc_t

    valid_bins = list(range(anchor, max_tier + 1))
    clamped = np.zeros(6)
    for i in valid_bins:
        clamped[i] = combined[i]

    underflow = sum(combined[:anchor])
    overflow = sum(combined[max_tier + 1:])
    clamped[anchor] += underflow
    clamped[max_tier] += overflow

    norm = clamped / clamped.sum() * 100
    norm = np.round(norm, 2)
    return norm.tolist()
