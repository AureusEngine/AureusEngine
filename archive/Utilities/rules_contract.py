# rules_contract_v3.py
# Canonical ruleset upgrade with explicit tier order and min/max continuous bin validation

QUALITY_ORDER = ["P", "C", "F", "X", "E", "Y"]
QUALITY_MAP = {q: i for i, q in enumerate(QUALITY_ORDER)}
REVERSE_QUALITY_MAP = {i: q for q, i in QUALITY_MAP.items()}

# -----------------------------
# Canonical Tier Functions
# -----------------------------

def get_canonical_tier_order():
    """Return immutable canonical tier order P→Y."""
    return QUALITY_ORDER


def tier_index(tier: str) -> int:
    """Return index of a tier in canonical order."""
    return QUALITY_MAP[tier]


def validate_min_max_continuous_bins(input_tiers: list[str], output_bins: dict[str, float]) -> bool:
    """Validate that output bins obey the continuous min/max rule based on input tiers."""
    min_tier_idx = min(tier_index(t) for t in input_tiers)
    max_tier_idx = max(tier_index(t) for t in input_tiers)

    # Build expected range
    expected_range = QUALITY_ORDER[min_tier_idx:max_tier_idx + 1]

    # 1. Check no bins below min or above max
    for i, tier in enumerate(QUALITY_ORDER):
        if tier not in expected_range and output_bins.get(tier, 0) > 0:
            return False

    # 2. Check continuous bins (no gaps inside range)
    non_zero_within = [tier for tier in expected_range if output_bins.get(tier, 0) > 0]
    return set(non_zero_within) == set(expected_range)


# -----------------------------
# Existing Functions (from v2)
# -----------------------------

def canonicalize_deviation(inputs: list[int]) -> tuple[int]:
    min_dev = min(inputs)
    return tuple(i - min_dev for i in inputs)


def normalize_deviation_signature_class(devsig: tuple[int], template_present: bool) -> tuple[frozenset, int | None]:
    base = frozenset(devsig[:-1]) if template_present else frozenset(devsig)
    template = devsig[-1] if template_present else None
    return (base, template)


def template_is_last(devsig: tuple[int], template_present: bool) -> bool:
    if not template_present:
        return False
    return True


def recipe_config_is_valid(qts: list[str], template_present: bool) -> bool:
    count = len(qts)
    if template_present:
        return count in (3, 4, 5)
    else:
        return count in (2, 3)


def nt_dataset_available(count: int) -> bool:
    return count <= 3


def bases_match_nt_to_template(nt_bases: frozenset, tpl_bases: frozenset) -> bool:
    return tpl_bases.issubset(nt_bases)


def output_respects_anchor_and_range(devsig: tuple[int], outputs: dict[str, float]) -> bool:
    anchor = min(devsig)
    max_dev = max(devsig)
    allowed = set(range(max_dev + 1))
    present = {
        i
        for i, k in enumerate(["Output_P", "Output_C", "Output_F", "Output_X", "Output_E", "Output_Y"])
        if outputs.get(k, 0.0) > 0.0
    }
    return present.issubset(allowed)


def output_has_no_internal_gaps(outputs: dict[str, float]) -> bool:
    bins = ["Output_P", "Output_C", "Output_F", "Output_X", "Output_E", "Output_Y"]
    started = False
    for b in bins:
        val = outputs.get(b, 0.0)
        if val > 0:
            started = True
        elif started and val == 0.0:
            remaining = [outputs.get(k, 0.0) for k in bins[bins.index(b)+1:]]
            if any(v > 0.0 for v in remaining):
                return False
    return True


def output_is_valid_distribution(devsig: tuple[int], outputs: dict[str, float]) -> bool:
    return output_respects_anchor_and_range(devsig, outputs) and output_has_no_internal_gaps(outputs)
