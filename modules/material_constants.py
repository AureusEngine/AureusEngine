
# material_constants.py

QUALITY_LABELS = ["P", "C", "R", "X", "E", "Y"]
QUALITY_SCORES = {"P": 1, "C": 2, "R": 3, "X": 4, "E": 5, "Y": 6}

WIN_LABEL = "W"
LOSS_LABEL = "L"

# Gear material requirements (subset example for structure)
STANDARD_GEAR_MATERIAL_REQUIREMENTS = {
    5: ["ADV", "BASE", "BASE", "TEMP"],
    10: ["ADV", "BASE", "BASE", "TEMP"],
    # ...
}

DRAGON_GEAR_MATERIAL_REQUIREMENTS = STANDARD_GEAR_MATERIAL_REQUIREMENTS.copy()

# etc.
