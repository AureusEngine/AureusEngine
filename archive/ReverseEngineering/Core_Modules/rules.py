# rules.py
# Canonical structural contracts for deviation signatures and shaping recipes

QUALITY_ORDER = ["P", "C", "F", "X", "E", "Y"]
QUALITY_MAP = {q: i for i, q in enumerate(QUALITY_ORDER)}
REVERSE_QUALITY_MAP = {i: q for q, i in QUALITY_MAP.items()}

# Canonical constraint: a recipe is at minimum QSF only if one or more QTs are at floor
def recipe_is_at_min_qsf(qt_list: list[str]) -> bool:
    return "P" in qt_list
