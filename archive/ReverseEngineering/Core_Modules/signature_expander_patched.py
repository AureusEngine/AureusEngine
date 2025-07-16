# Signature Expander for Aureus Engine
# Generates all valid material combinations that match a given deviation signature
# Respects template-role placement and anchor/max quality constraints

from typing import List, Tuple, Optional, Dict, Union
import itertools
from deviation import compute_deviation_signature

QUALITY_INDEX = {
    "P": 0, "C": 1, "F": 2, "X": 3, "E": 4, "Y": 5
}

QUALITY_LABELS = {
    0: "P", 1: "C", 2: "F", 3: "X", 4: "E", 5: "Y"
}

def expand_signature(
    signature: Optional[Tuple[int, ...]] = None,
    Q_anchor: Optional[int] = None,
    qualities: Optional[List[str]] = None,
    quality_string: Optional[str] = None,
    template_index: Optional[int] = None,
    Q_max: int = 5,
    verbose: bool = False,
    preserve_order: bool = False,
    output_mode: str = "canonical",  # options: "canonical", "flat", "ui"
    expand_tiers: bool = False,
    combinatoric: bool = True
) -> Union[List[Dict], Dict]:
    """
    Signature Expander Utility

    Accepts canonical deviation signature or derives one from quality inputs.
    Expands all valid permutations within constraints and renders results in
    multiple formats (raw, canonical, or UI-facing).
    """

    if (qualities or quality_string) and (signature or Q_anchor):
        raise ValueError("Provide either (qualities or quality_string) OR (signature and Q_anchor), not both.")

    if quality_string:
        qualities = list(quality_string.upper())

    if qualities:
        profile = compute_deviation_signature(qualities, template_index)
        signature = profile["signature"]
        Q_anchor = profile["Q_shift"]
        template_index = profile["template_index"]

    if signature is None or Q_anchor is None:
        raise ValueError("Must provide either signature + Q_anchor, or qualities/quality_string with optional template_index.")

    if 0 not in signature:
        raise ValueError("Invalid deviation signature: must include at least one zero (anchor-aligned input).")

    num_materials = len(signature)
    base_devs = list(signature[:-1])
    dev_template = signature[-1]
    results = []

    anchor_range = [Q_anchor] if not expand_tiers else list(range(0, Q_max - max(signature) + 1))

    for anchor in anchor_range:
        output = []
        rejected = 0
        base_perms = set(itertools.permutations(base_devs)) if combinatoric else {tuple(base_devs)}

        if dev_template == 0:
            for base in base_perms:
                for t_pos in range(num_materials):
                    devs = list(base)
                    devs.insert(t_pos, dev_template)
                    Q_values = [anchor + d for d in devs]
                    if all(anchor <= q <= Q_max for q in Q_values):
                        if preserve_order:
                            devs_canonical = [q - anchor for q in Q_values]
                            results.append({
                                "Q_values": Q_values,
                                "labels": [QUALITY_LABELS[q] for q in Q_values],
                                "template_index": t_pos,
                                "signature": tuple(devs_canonical)
                            })
                        else:
                            q_copy = Q_values.copy()
                            q_template = q_copy.pop(t_pos)
                            q_copy.append(q_template)
                            devs_canonical = [q - min(q_copy) for q in q_copy]
                            results.append({
                                "Q_values": q_copy,
                                "labels": [QUALITY_LABELS[q] for q in q_copy],
                                "template_index": num_materials - 1,
                                "signature": tuple(devs_canonical)
                            })
                    else:
                        rejected += 1
        else:
            for base in base_perms:
                devs = list(base) + [dev_template]
                Q_values = [anchor + d for d in devs]
                if all(anchor <= q <= Q_max for q in Q_values):
                    labels = [QUALITY_LABELS[q] for q in Q_values]
                    results.append({
                        "Q_values": Q_values,
                        "labels": labels,
                        "template_index": num_materials - 1,
                        "signature": tuple(devs)
                    })
                else:
                    rejected += 1

    seen = set()
    deduped_output = []
    for entry in results:
        key = (tuple(entry["Q_values"]), entry["template_index"])
        if key not in seen:
            seen.add(key)
            deduped_output.append(entry)

    if verbose:
        print(f"[SignatureExpander] Generated {len(deduped_output)} combinations.")

    if output_mode == "canonical":
        return {
            "signature": signature,
            "Q_anchor": Q_anchor,
            "combinations": deduped_output
        }
    elif output_mode == "ui":
        return [
            f"{' + '.join(sorted(entry['labels'][:entry['template_index']] + entry['labels'][entry['template_index']+1:], key=lambda x: QUALITY_INDEX[x]))} + {entry['labels'][entry['template_index']]} (template)"
            for entry in deduped_output
        ]
    else:
        return deduped_output


# Applies a uniform QSF shift to a deviation signature
def apply_qsf_shift(dev_sig: list[int], shift: int) -> list[int]:
    return [v + shift for v in dev_sig]
