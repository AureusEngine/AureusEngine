# kernel_rules.py
# Empirical rules and shaping behavior logic derived from canonical observations
# Used by shaping_kernel.py to inform prediction logic and bin weighting behavior

TEMPLATE_BIASES = {
    "P": 0.0,
    "C": 0.1,
    "F": 0.25,
    "X": 0.4,
    "E": 0.55,
    "Y": 0.7
}

QUALITY_ORDER = ["P", "C", "F", "X", "E", "Y"]
QUALITY_MAP = {q: i for i, q in enumerate(QUALITY_ORDER)}
REVERSE_QUALITY_MAP = {i: q for q, i in QUALITY_MAP.items()}

# Clamp predicted quality index to valid range (0–5)
def clamp_quality_index(index: float) -> int:
    return max(0, min(5, round(index)))

# Detect shaping curve region based on deviation signature magnitude
def shaping_curve_regime(dev_sig: list[int]) -> str:
    total_mag = sum(abs(v) for v in dev_sig)
    if total_mag <= 3:
        return "mid-arc"
    elif total_mag >= 8:
        return "hard-edge"
    return "soft-slope"

# Get template intercept shift used in shaping regression curve
def template_bias(template: str) -> float:
    return TEMPLATE_BIASES.get(template, 0.0)

# Heuristic to detect if template likely causes bin reversal
def is_template_reversal_zone(template: str, dev_sig: list[int]) -> bool:
    return template in {"X", "Y"} and max(dev_sig) >= 4 and dev_sig.count(0) >= 1

# Predict fallback quality index for simple baseline shaping
def default_shape_quality_index(dev_sig: list[int], template: str) -> float:
    base_score = 0.5 * dev_sig[0] + 1.0 * dev_sig[1] + 0.75 * dev_sig[2]
    return base_score + template_bias(template)

# Check if a deviation signature is in a known saturation zone
def is_saturated(dev_sig: list[int]) -> bool:
    return sum(dev_sig) >= 10 or any(v >= 5 for v in dev_sig)

# Convert quality label to index
def quality_to_index(q: str) -> int:
    return QUALITY_MAP[q]

def index_to_quality(i: int) -> str:
    return REVERSE_QUALITY_MAP[clamp_quality_index(i)]

# Estimate template-induced shaping shift vector
def estimate_template_shift(dev_sig: list[int]) -> list[float]:
    if dev_sig == [0, 0, 1]:
        return [-15.87, 15.87, 0.0, 0.0, 0.0, 0.0]
    elif dev_sig == [0, 0, 2]:
        return [-12.12, -2.02, 14.14, 0.0, 0.0, 0.0]
    elif dev_sig == [0, 1, 2]:
        return [-8.08, -6.06, 14.14, 0.0, 0.0, 0.0]
    elif dev_sig == [0, 1, 3]:
        return [-5.96, -4.76, -1.19, 11.9, 0.0, 0.0]
    return [0.0] * 6

# Enforce strict positional interpretation of deviation signature
def is_strictly_positional(dev_sig: list[int]) -> bool:
    return isinstance(dev_sig, list) and len(dev_sig) == 3

# Rejects deviation signatures that apply bin symmetry or non-positional inference
def rejects_symmetry_based_normalization() -> bool:
    return True  # This kernel operates on strict (Input1, Input2, Template) ordering only

# Structural rule: any recipe composed of QT's that does not include at least one "P"
# cannot possibly be QSF-minimized. This is a canonical constraint.
def recipe_is_at_min_qsf(qt_list: list[str]) -> bool:
    return "P" in qt_list
