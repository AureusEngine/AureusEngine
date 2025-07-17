# dataset_normalizer.py
# Utility module to shift all recipe inputs to lowest possible QSF (d0 = P)
# and normalize the associated deviation signatures accordingly

from Core_Modules.signature_expander import apply_qsf_shift
from Core_Modules.deviation import get_deviation_signature
from Core_Modules.quality_map import QUALITY_ORDER, QUALITY_MAP, index_to_quality


def normalize_to_p_devsig(entry: dict) -> dict:
    """
    Returns a normalized version of the entry where the lowest input QT is P,
    and the deviation signature reflects that.
    """
    qt_inputs = [entry["Input1"], entry["Input2"], entry["Template"]]
    qt_indices = [QUALITY_MAP[q] for q in qt_inputs]

    # Determine the minimum QT index to calculate the required shift
    min_qt_index = min(qt_indices)
    shift_required = min_qt_index  # number of steps to shift all inputs down to make d0 = P

    # If already at minimum, no shift needed
    if shift_required == 0:
        return entry

    # De-normalize the signature by re-expanding it
    current_devsig = entry["DeviationSignature"]
    denormalized_devsig = [v + shift_required for v in current_devsig]

    # Shift the deviation signature back down
    new_devsig = apply_qsf_shift(denormalized_devsig, -shift_required)

    # Shift the QTs down accordingly
    new_inputs = [index_to_quality(idx - shift_required) for idx in qt_indices]

    return {
        **entry,
        "Input1": new_inputs[0],
        "Input2": new_inputs[1],
        "Template": new_inputs[2],
        "Recipe": "".join(new_inputs),
        "DeviationSignature": new_devsig
    }


def normalize_dataset(entries: list[dict]) -> list[dict]:
    """
    Normalize an entire dataset to enforce lowest QT = P and correct devsig.
    """
    return [normalize_to_p_devsig(entry) for entry in entries]
