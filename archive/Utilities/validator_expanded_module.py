
import json

# Canonical tier order
TIERS = ["P", "C", "F", "X", "E", "Y"]

def validate_expanded_dataset(input_path):
    '''
    Validate expanded dataset for canonical compliance:
    - No tier > 5
    - Continuous bins between min and max
    - Proper fields present
    '''
    with open(input_path) as f:
        expanded_data = json.load(f)

    invalid_tiers = []
    bins_errors = []
    missing_fields = []

    required_fields = [
        "Recipe", "BaseSignatureSorted", "TemplateDevAbsolute", "TemplateDevRelative",
        "TemplatePresent", "OutputBins", "IsNormalized", "ShiftValue", "OriginalRecipe"
    ]

    for e in expanded_data:
        # Check required fields
        for field in required_fields:
            if field not in e:
                missing_fields.append({"Recipe": e.get("Recipe", None), "MissingField": field})

        # Tier limit check
        if any(v > 5 for v in e["BaseSignatureSorted"]) or e["TemplateDevAbsolute"] > 5:
            invalid_tiers.append(e)

        # Continuity check
        min_val = min(e["BaseSignatureSorted"] + [e["TemplateDevAbsolute"]])
        max_val = max(e["BaseSignatureSorted"] + [e["TemplateDevAbsolute"]])
        for idx, tier in enumerate(TIERS[min_val:max_val+1], start=min_val):
            if e["OutputBins"][tier] == 0.0:
                bins_errors.append({
                    "Recipe": e["Recipe"],
                    "ShiftValue": e["ShiftValue"],
                    "Issue": f"Zero bin within continuous range {tier}"
                })

    return {
        "total_entries": len(expanded_data),
        "invalid_tiers": len(invalid_tiers),
        "continuity_errors": len(bins_errors),
        "missing_fields": len(missing_fields)
    }

# Usage Example:
# results = validate_expanded_dataset("3mat_template_EXPANDED.json")
# print(results)
