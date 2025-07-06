
# Centralized repository for quality and material weight constants

QUALITY_LABELS = ["P", "C", "R", "X", "E", "Y"]
QUALITY_SCORES = {"P": 1, "C": 2, "R": 3, "X": 4, "E": 5, "Y": 6}

MATERIAL_WEIGHTS = {
    "BASE": 1.0,
    "ADV": 1.0,
    "TEMP": 1.5
}

# Template position weights for emphasis in prediction
TEMPLATE_POSITION_WEIGHT = 2.0
