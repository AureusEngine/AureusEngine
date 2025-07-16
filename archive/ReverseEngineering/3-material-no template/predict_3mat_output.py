
from shaping_kernel_3mat import generate_shaping_curve
from adjustment_kernel_3mat import apply_adjustment

def predict_distribution(dev_signature):
    curve = generate_shaping_curve(dev_signature)
    min_tier = 0
    max_tier = max(dev_signature)
    return apply_adjustment(curve, min_tier, max_tier)
