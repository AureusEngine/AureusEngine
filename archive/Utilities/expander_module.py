
import json

# Canonical tier order
TIERS = ["P", "C", "F", "X", "E", "Y"]

def recipe_to_indices(recipe):
    return [TIERS.index(ch) for ch in recipe]

def indices_to_recipe(indices):
    return "".join(TIERS[min(i, 5)] for i in indices)

def expand_template_dataset(input_path, output_path):
    '''
    Expand a template-inclusive dataset (3-mat or 4-mat) by shifting tier values
    up to Y (5) while preserving canonical rules and generating dual template fields.
    '''
    with open(input_path) as f:
        dataset = json.load(f)

    expanded_entries = []

    for entry in dataset:
        # Determine base signature sorted
        base_sorted = sorted(entry.get("BaseSignature", entry.get("BaseSignatureSorted", [])))
        template_dev = entry["TemplateDev"]

        for shift in range(0, 6):
            # Stop if any value exceeds tier 5
            if max(base_sorted + [template_dev]) + shift > 5:
                break

            # Shift recipe
            recipe_indices = recipe_to_indices(entry["Recipe"])
            shifted_recipe = indices_to_recipe([i + shift for i in recipe_indices])

            # Shift bases and template
            shifted_bases = [v + shift for v in base_sorted]
            template_dev_absolute = template_dev + shift

            # Compute relative template deviation
            lowest_value = min(shifted_bases + [template_dev_absolute])
            template_dev_relative = template_dev_absolute - lowest_value

            # Shift bins upward
            shifted_bins = {tier: 0.0 for tier in TIERS}
            for i, tier in enumerate(TIERS):
                target_index = i + shift
                if target_index >= len(TIERS):
                    break
                shifted_bins[TIERS[target_index]] += entry["OutputBins"][tier]

            # Zero out outside min/max
            min_val = min(shifted_bases + [template_dev_absolute])
            max_val = max(shifted_bases + [template_dev_absolute])
            for i, tier in enumerate(TIERS):
                if i < min_val or i > max_val:
                    shifted_bins[tier] = 0.0

            # Build expanded entry
            expanded_entry = {
                "Recipe": shifted_recipe,
                "BaseSignatureSorted": shifted_bases,
                "TemplateDevAbsolute": template_dev_absolute,
                "TemplateDevRelative": template_dev_relative,
                "TemplatePresent": True,
                "OutputBins": shifted_bins,
                "IsNormalized": shift == 0,
                "ShiftValue": shift,
                "OriginalRecipe": entry["Recipe"]
            }
            expanded_entries.append(expanded_entry)

    with open(output_path, "w") as f:
        json.dump(expanded_entries, f, indent=2)

    return expanded_entries

def validate_expanded_dataset(expanded_data):
    '''
    Validate expanded dataset for canonical compliance:
    - No tier > 5
    - Continuous bins between min and max
    - Proper fields present
    '''
    invalid_tiers = []
    bins_errors = []

    for e in expanded_data:
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
        "continuity_errors": len(bins_errors)
    }

# Usage Example:
# expanded = expand_template_dataset("3mat_template_UNIFIED_SORTED.json", "3mat_template_EXPANDED.json")
# results = validate_expanded_dataset(expanded)
# print(results)
