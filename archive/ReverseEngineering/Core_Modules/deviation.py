# deviation.py
# Module: Deviation Signature Profiler
# Purpose: Extracts canonical deviation signature, template index, and anchor shift metadata

from typing import List, Dict, Optional, Tuple

QUALITY_INDEX = {
    "P": 0, "C": 1, "F": 2, "X": 3, "E": 4, "Y": 5
}

QUALITY_LABELS = {
    0: "P", 1: "C", 2: "F", 3: "X", 4: "E", 5: "Y"
}

def compute_deviation_signature(qualities: List[str], template_index: Optional[int] = None) -> Dict:
    """
    Computes a normalized deviation signature from material quality labels.

    Parameters:
        qualities (List[str]): Quality labels (e.g. ["F", "X", "E"])
        template_index (Optional[int]): Index of template material if present

    Returns:
        Dict with:
            - "signature": Tuple[int, ...] with last element = template deviation
            - "Q_shift": int original anchor (used for restoration or expansion)
            - "Q_anchor": int minimum Q value in original input
            - "Q_max": int maximum Q value in original input
            - "Q_values": List[int] of raw Q inputs
            - "labels": List[str] identical to input
            - "template_index": index of template (unchanged)
            - "uniform": bool whether all inputs are same Q
    """
    Q_values = [QUALITY_INDEX[q] for q in qualities]
    Q_anchor = min(Q_values)
    Q_shift = Q_anchor
    Q_max = max(Q_values)
    uniform = all(q == Q_anchor for q in Q_values)

    deviations = [q - Q_anchor for q in Q_values]

    if template_index is not None:
        dev_template = deviations.pop(template_index)
        deviations.append(dev_template)

    return {
        "signature": tuple(deviations),
        "Q_shift": Q_shift,
        "Q_anchor": Q_anchor,
        "Q_max": Q_max,
        "Q_values": Q_values,
        "labels": qualities,
        "template_index": template_index,
        "uniform": uniform
    }
