# rules.py
# Canonical structural contract for the Aureus Engine shaping system

from typing import List, Tuple

# ----------------------
# 1. Quality Tier Mapping
# ----------------------

QUALITY_INDEX = { "P": 0, "C": 1, "F": 2, "X": 3, "E": 4, "Y": 5 }
QUALITY_LABELS = { v: k for k, v in QUALITY_INDEX.items() }
MAX_QUALITY = 5

# ----------------------
# 2. Valid Deviation Signature
# ----------------------

def is_valid_signature(sig: Tuple[int, ...]) -> bool:
    """A valid deviation signature must contain at least one zero."""
    return 0 in sig

# ----------------------
# 3. Template Role Rules
# ----------------------

def is_template_flexible(sig: Tuple[int, ...]) -> bool:
    """
    If the template deviation is zero, the template is interchangeable.
    Otherwise, it is fixed at the final index.
    NOTE: May be deprecated post reverse-engineering in favor of hard lock on template-last.
    """
    return sig[-1] == 0

# ----------------------
# 4. Anchor Detection
# ----------------------

def get_anchor(Q_values: List[int]) -> int:
    """Returns the lowest quality value in the recipe."""
    return min(Q_values)

# ----------------------
# 5. Tier Boundary Enforcement
# ----------------------

def valid_Q_range(Q_values: List[int]) -> bool:
    """Ensures all Q values are within valid bounds [0–5]."""
    return all(0 <= q <= MAX_QUALITY for q in Q_values)

# ----------------------
# 5.1. Provisional: No Gaps in Interior Bins
# ----------------------

def has_internal_zero_gap(distribution: List[float]) -> bool:
    """
    Returns True if a zero exists between two non-zero bins.
    Used to test for illegal gaps inside the distribution curve.
    NOTE: This rule is provisional and will be verified against canonical data.
    """
    non_zero_indices = [i for i, val in enumerate(distribution) if val > 0]
    if len(non_zero_indices) < 2:
        return False
    return any(distribution[i] == 0 for i in range(non_zero_indices[0]+1, non_zero_indices[-1]))

# ----------------------
# 6. Base Order Invariance
# ----------------------

def is_order_invariant(a: List[int], b: List[int]) -> bool:
    """Checks whether two base sequences are order-equivalent."""
    return sorted(a) == sorted(b)

# ----------------------
# 7. Valid Anchor Range for Tier-Shift
# ----------------------

def valid_anchor_range(signature: Tuple[int, ...]) -> List[int]:
    """
    Computes all valid Q_anchor values that keep signature within bounds.
    NOTE: May need refinement to incorporate valid tier wrapping in edge cases.
    """
    max_dev = max(signature)
    return list(range(0, MAX_QUALITY - max_dev + 1))

# ----------------------
# 8. Seed Validation Rules
# ----------------------

def validate_recipe(signature: Tuple[int, ...], Q_values: List[int]) -> bool:
    """
    Applies hard rules to validate seeds, not intermediate tier shifts.
    - Signature must contain a 0
    - All Q values must be within bounds
    """
    return is_valid_signature(signature) and valid_Q_range(Q_values)

# ----------------------
# 9. Canonicalization of Signatures
# ----------------------

def canonicalize_deviation(Q_values: List[int], template_index: int) -> Tuple[int, ...]:
    """Normalizes Q values to deviation signature with template deviation last."""
    anchor = min(Q_values)
    deviations = [q - anchor for q in Q_values]
    dev_template = deviations.pop(template_index)
    deviations.append(dev_template)
    return tuple(deviations)

# ----------------------
# 10. Recipe Type from Signature
# ----------------------

def recipe_type_from_signature(signature: Tuple[int, ...]) -> str:
    """Infers recipe structure from signature length."""
    return {2: "2-material", 3: "3-material", 4: "4-material", 5: "5-material"}.get(len(signature), "Unknown")

# ----------------------
# 11. Uniformity Check
# ----------------------

def is_uniform(Q_values: List[int]) -> bool:
    """Detects whether all qualities are identical."""
    return all(q == Q_values[0] for q in Q_values)

# ----------------------
# 12. Deduplication Rule
# ----------------------
# Applied structurally in expander: deduplicate by (Q_values, template_index)

# ----------------------
# 13. UI Display Guidelines
# ----------------------
# Template always appears last for readability; base order can be sorted optionally.

# ----------------------
# 14. Reverse Reconstruction
# ----------------------

def reconstruct_from_signature(signature: Tuple[int, ...], Q_anchor: int) -> List[int]:
    """Rebuilds raw Q values from a deviation signature and anchor."""
    return [Q_anchor + d for d in signature]
