
def fit_to_canonical_profile(generated, canonical):
    """
    Measures deviation between generated and canonical profiles using MAE.
    """
    return sum(abs(g - c) for g, c in zip(generated, canonical)) / len(canonical)
