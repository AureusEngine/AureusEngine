
import json
from collections import Counter

TIER_ORDER = ["P", "C", "F", "X", "E", "Y"]
TIER_MAP = {t: i for i, t in enumerate(TIER_ORDER)}

def load_dataset(path):
    with open(path, "r") as f:
        return json.load(f)

def validate_distribution_sum(entry, tolerance=0.01):
    total = sum(entry[f"Output_{t}"] for t in TIER_ORDER)
    return abs(total - 100.0) <= tolerance
def validate_output_range(entry):
    inputs = [entry[f"Input{i+1}"] for i in range(4) if f"Input{i+1}" in entry] + [entry["Template"]]
    min_tier = min(TIER_MAP[t] for t in inputs)
    max_tier = max(TIER_MAP[t] for t in inputs)
    return all(
        (entry[f"Output_{TIER_ORDER[i]}"] == 0)
        for i in range(len(TIER_ORDER))
        if i < min_tier or i > max_tier
    )

def validate_no_intermediate_zero(entry):
    inputs = [entry[f"Input{i+1}"] for i in range(4) if f"Input{i+1}" in entry] + [entry["Template"]]
    min_tier = min(TIER_MAP[t] for t in inputs)
    max_tier = max(TIER_MAP[t] for t in inputs)
    return all(entry[f"Output_{TIER_ORDER[i]}"] > 0 for i in range(min_tier, max_tier + 1))

def validate_uniform_output(entry):
    material_fields = [f"Input{i+1}" for i in range(4) if f"Input{i+1}" in entry] + ["Template"]
    materials = [entry[f] for f in material_fields]
    if all(mat == materials[0] for mat in materials):
        for t in TIER_ORDER:
            expected = 100.0 if t == materials[0] else 0.0
            if round(entry[f"Output_{t}"], 2) != expected:
                return False
    return True

def find_outlier_values(dataset, threshold=1):
    values = [round(entry[f"Output_{t}"], 2) for entry in dataset for t in TIER_ORDER]
    freq = Counter(values)
    return [v for v, count in freq.items() if count <= threshold]

def validate_dataset(dataset):
    results = {
        "sum_errors": [],
        "range_errors": [],
        "intermediate_zero_errors": [],
        "uniform_errors": [],
        "rare_values": find_outlier_values(dataset)
    }
    for entry in dataset:
        recipe = entry["Recipe"]
        if not validate_distribution_sum(entry):
            results["sum_errors"].append(recipe)
        if not validate_output_range(entry):
            results["range_errors"].append(recipe)
        if not validate_no_intermediate_zero(entry):
            results["intermediate_zero_errors"].append(recipe)
        if not validate_uniform_output(entry):
            results["uniform_errors"].append(recipe)
    return results


from kernel_rules import QUALITY_MAP, estimate_qsf_from_inputs, is_upshifted_recipe

def validate_qsf_alignment(entry):
    input1 = entry["Input1"]
    input2 = entry["Input2"]
    template = entry["Template"]
    devsig = entry["DeviationSignature"]

    q1, q2, qt = QUALITY_MAP[input1], QUALITY_MAP[input2], QUALITY_MAP[template]
    d0, d1, d2 = devsig

    # Check if signature is logically invalid
    reconstructed = [q1 - d0, q2 - d1, qt - d2]
    if any(val < 0 or val > 5 for val in reconstructed):
        return "INVALID_DEV_SIG_ALIGNMENT"

    # Check if inputs could be shifted downward
    if is_upshifted_recipe(input1, input2, template):
        return "VALID_BUT_UPSHIFTED"

    return None
