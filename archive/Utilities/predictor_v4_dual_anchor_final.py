"""
predictor_v4.py
Predictor for 2-, 3-, and 4-mat recipes with canonical normalization and template bias handling.

Key logic:
- Bases are mock-normalized (min = 0) for NT lookup.
- Template deviation remains absolute (never normalized).
- After lookup, baseline bins are shifted upward by original base offset.
- Template bias is applied on top of shifted baseline.
- Continuous min/max rule enforced; output normalized to 100%.
"""

from rules_contract_v3 import (
    get_canonical_tier_order,
    validate_min_max_continuous_bins
)

TEMPLATE_DELTAS = {
    ((0, 0), 0): {'Delta_P': -60.87, 'Delta_C': 17.39, 'Delta_F': 13.04, 'Delta_X': 8.7, 'Delta_E': 4.35, 'Delta_Y': 17.39},
    ((0, 0), 1): {'Delta_P': -44.44, 'Delta_C': 44.44, 'Delta_F': 0.0, 'Delta_X': 0.0, 'Delta_E': 0.0, 'Delta_Y': 0.0},
    ((0, 0), 2): {'Delta_P': -45.45, 'Delta_C': 9.09, 'Delta_F': 36.36, 'Delta_X': 0.0, 'Delta_E': 0.0, 'Delta_Y': 0.0},
    ((0, 0), 3): {'Delta_P': -50.0, 'Delta_C': 14.29, 'Delta_F': 7.14, 'Delta_X': 28.57, 'Delta_E': 0.0, 'Delta_Y': 0.0},
    ((0, 0), 4): {'Delta_P': -55.56, 'Delta_C': 16.67, 'Delta_F': 11.11, 'Delta_X': 5.56, 'Delta_E': 22.22, 'Delta_Y': 0.0},
    ((0, 0), 5): {'Delta_P': -60.87, 'Delta_C': 17.39, 'Delta_F': 13.04, 'Delta_X': 8.7, 'Delta_E': 4.35, 'Delta_Y': 17.39},
    ((0, 1), 0): {'Delta_P': -20.87, 'Delta_C': -22.61, 'Delta_F': 13.04, 'Delta_X': 8.7, 'Delta_E': 13.04, 'Delta_Y': 8.7},
    ((0, 1), 1): {'Delta_P': -26.67, 'Delta_C': 26.67, 'Delta_F': 0.0, 'Delta_X': 0.0, 'Delta_E': 0.0, 'Delta_Y': 0.0},
    ((0, 1), 2): {'Delta_P': -23.64, 'Delta_C': -12.73, 'Delta_F': 36.36, 'Delta_X': 0.0, 'Delta_E': 0.0, 'Delta_Y': 0.0},
    ((0, 1), 3): {'Delta_P': -24.29, 'Delta_C': -11.43, 'Delta_F': 7.14, 'Delta_X': 28.57, 'Delta_E': 0.0, 'Delta_Y': 0.0},
    ((0, 1), 4): {'Delta_P': -26.67, 'Delta_C': -12.22, 'Delta_F': 11.11, 'Delta_X': 5.56, 'Delta_E': 22.22, 'Delta_Y': 0.0},
    ((0, 1), 5): {'Delta_P': -29.57, 'Delta_C': -13.91, 'Delta_F': 13.04, 'Delta_X': 8.7, 'Delta_E': 4.35, 'Delta_Y': 17.39},
    ((0, 2), 0): {'Delta_P': -18.01, 'Delta_C': 3.1, 'Delta_F': -15.53, 'Delta_X': 17.39, 'Delta_E': 4.35, 'Delta_Y': 8.7},
    ((0, 2), 1): {'Delta_P': -20.78, 'Delta_C': 31.16, 'Delta_F': -10.39, 'Delta_X': 0.0, 'Delta_E': 0.0, 'Delta_Y': 0.0},
    ((0, 2), 2): {'Delta_P': -20.78, 'Delta_C': -5.2, 'Delta_F': 25.98, 'Delta_X': 0.0, 'Delta_E': 0.0, 'Delta_Y': 0.0},
    ((0, 2), 3): {'Delta_P': -21.43, 'Delta_C': 0.0, 'Delta_F': -7.14, 'Delta_X': 28.57, 'Delta_E': 0.0, 'Delta_Y': 0.0},
    ((0, 2), 4): {'Delta_P': -23.81, 'Delta_C': 2.38, 'Delta_F': -6.35, 'Delta_X': 5.56, 'Delta_E': 22.22, 'Delta_Y': 0.0},
    ((0, 2), 5): {'Delta_P': -26.71, 'Delta_C': 3.1, 'Delta_F': -6.83, 'Delta_X': 8.7, 'Delta_E': 4.35, 'Delta_Y': 17.39},
    ((0, 3), 0): {'Delta_P': -10.87, 'Delta_C': -2.61, 'Delta_F': 11.74, 'Delta_X': -11.3, 'Delta_E': 4.35, 'Delta_Y': 8.7},
    ((0, 3), 1): {'Delta_P': -14.29, 'Delta_C': 22.86, 'Delta_F': -2.86, 'Delta_X': -5.71, 'Delta_E': 0.0, 'Delta_Y': 0.0},
    ((0, 3), 2): {'Delta_P': -14.29, 'Delta_C': -5.71, 'Delta_F': 25.71, 'Delta_X': -5.71, 'Delta_E': 0.0, 'Delta_Y': 0.0},
    ((0, 3), 3): {'Delta_P': -14.29, 'Delta_C': -5.71, 'Delta_F': -2.86, 'Delta_X': 22.86, 'Delta_E': 0.0, 'Delta_Y': 0.0},
    ((0, 3), 4): {'Delta_P': -16.67, 'Delta_C': -3.33, 'Delta_F': 1.11, 'Delta_X': -3.33, 'Delta_E': 22.22, 'Delta_Y': 0.0},
    ((0, 3), 5): {'Delta_P': -19.57, 'Delta_C': -2.61, 'Delta_F': 3.04, 'Delta_X': -2.61, 'Delta_E': 4.35, 'Delta_Y': 17.39},
    ((0, 4), 0): {'Delta_P': -3.73, 'Delta_C': 4.66, 'Delta_F': -1.25, 'Delta_X': 1.56, 'Delta_E': -9.94, 'Delta_Y': 8.7},
    ((0, 4), 1): {'Delta_P': -9.53, 'Delta_C': 17.46, 'Delta_F': -3.18, 'Delta_X': -1.58, 'Delta_E': -3.18, 'Delta_Y': 0.0},
    ((0, 4), 2): {'Delta_P': -9.53, 'Delta_C': -4.76, 'Delta_F': 19.04, 'Delta_X': -1.58, 'Delta_E': -3.18, 'Delta_Y': 0.0},
    ((0, 4), 3): {'Delta_P': -9.53, 'Delta_C': -4.76, 'Delta_F': -3.18, 'Delta_X': 20.64, 'Delta_E': -3.18, 'Delta_Y': 0.0},
    ((0, 4), 4): {'Delta_P': -9.53, 'Delta_C': -4.76, 'Delta_F': -3.18, 'Delta_X': -1.58, 'Delta_E': 19.04, 'Delta_Y': 0.0},
    ((0, 4), 5): {'Delta_P': -12.43, 'Delta_C': -4.04, 'Delta_F': -1.25, 'Delta_X': 1.56, 'Delta_E': -1.25, 'Delta_Y': 17.39},
    ((0, 5), 0): {'Delta_P': 10.99, 'Delta_C': -3.66, 'Delta_F': -2.75, 'Delta_X': -1.83, 'Delta_E': -0.91, 'Delta_Y': -1.83},
    ((0, 5), 1): {'Delta_P': -6.41, 'Delta_C': 13.73, 'Delta_F': -2.75, 'Delta_X': -1.83, 'Delta_E': -0.91, 'Delta_Y': -1.83},
    ((0, 5), 2): {'Delta_P': -6.41, 'Delta_C': -3.66, 'Delta_F': 14.64, 'Delta_X': -1.83, 'Delta_E': -0.91, 'Delta_Y': -1.83},
    ((0, 5), 3): {'Delta_P': -6.41, 'Delta_C': -3.66, 'Delta_F': -2.75, 'Delta_X': 15.56, 'Delta_E': -0.91, 'Delta_Y': -1.83},
    ((0, 5), 4): {'Delta_P': -6.41, 'Delta_C': -3.66, 'Delta_F': -2.75, 'Delta_X': -1.83, 'Delta_E': 16.48, 'Delta_Y': -1.83},
    ((0, 5), 5): {'Delta_P': -6.41, 'Delta_C': -3.66, 'Delta_F': -2.75, 'Delta_X': -1.83, 'Delta_E': -0.91, 'Delta_Y': 15.56},
    ((0, 0, 4), 3): {'Delta_P': -13.64, 'Delta_C': -5.11, 'Delta_F': -3.41, 'Delta_X': 25.57, 'Delta_E': -3.41, 'Delta_Y': 0.0},
    ((0, 0, 0), 0): {'Delta_P': -46.67, 'Delta_C': 6.67, 'Delta_F': 40.0, 'Delta_X': 0.0, 'Delta_E': 0.0, 'Delta_Y': 0.0},
    ((0, 2, 2), 1): {'Delta_P': -17.77, 'Delta_C': 35.56, 'Delta_F': -17.77, 'Delta_X': 0.0, 'Delta_E': 0.0, 'Delta_Y': 0.0},
    ((0, 4, 4), 0): {'Delta_P': 3.24, 'Delta_C': 3.47, 'Delta_F': -1.39, 'Delta_X': 1.16, 'Delta_E': -21.3, 'Delta_Y': 14.81},
    ((0, 0, 0), 1): {'Delta_P': -46.15, 'Delta_C': 46.15, 'Delta_F': 0.0, 'Delta_X': 0.0, 'Delta_E': 0.0, 'Delta_Y': 0.0},
    ((0, 0, 0), 3): {'Delta_P': -50.0, 'Delta_C': 11.11, 'Delta_F': 5.56, 'Delta_X': 33.33, 'Delta_E': 0.0, 'Delta_Y': 0.0},
    ((0, 2, 2), 5): {'Delta_P': -18.51, 'Delta_C': 3.7, 'Delta_F': -18.51, 'Delta_X': 7.41, 'Delta_E': 3.7, 'Delta_Y': 22.22},
    ((0, 1, 4), 0): {'Delta_P': 17.05, 'Delta_C': -8.52, 'Delta_F': -3.41, 'Delta_X': -1.7, 'Delta_E': -3.41, 'Delta_Y': 0.0},
    ((0, 1, 3), 5): {'Delta_P': -15.74, 'Delta_C': -11.11, 'Delta_F': 2.78, 'Delta_X': -1.86, 'Delta_E': 3.7, 'Delta_Y': 22.22},
    ((0, 0, 1), 3): {'Delta_P': -32.54, 'Delta_C': -6.35, 'Delta_F': 5.56, 'Delta_X': 33.33, 'Delta_E': 0.0, 'Delta_Y': 0.0},
    ((0, 0, 0), 5): {'Delta_P': -59.26, 'Delta_C': 14.81, 'Delta_F': 11.11, 'Delta_X': 7.41, 'Delta_E': 3.7, 'Delta_Y': 22.22},
    ((0, 0, 0), 2): {'Delta_P': -46.67, 'Delta_C': 6.67, 'Delta_F': 40.0, 'Delta_X': 0.0, 'Delta_E': 0.0, 'Delta_Y': 0.0},
    ((0, 0, 0), 4): {'Delta_P': -54.55, 'Delta_C': 13.64, 'Delta_F': 9.09, 'Delta_X': 4.55, 'Delta_E': 27.27, 'Delta_Y': 0.0},
    ((0, 0, 1), 1): {'Delta_P': -32.97, 'Delta_C': 32.97, 'Delta_F': 0.0, 'Delta_X': 0.0, 'Delta_E': 0.0, 'Delta_Y': 0.0},
    ((0, 0, 1), 4): {'Delta_P': -35.07, 'Delta_C': -5.84, 'Delta_F': 9.09, 'Delta_X': 4.55, 'Delta_E': 27.27, 'Delta_Y': 0.0},
    ((0, 0, 3), 5): {'Delta_P': -25.0, 'Delta_C': -1.86, 'Delta_F': 2.78, 'Delta_X': -1.86, 'Delta_E': 3.72, 'Delta_Y': 22.22},
    ((0, 0, 1), 5): {'Delta_P': -38.1, 'Delta_C': -6.35, 'Delta_F': 11.11, 'Delta_X': 7.41, 'Delta_E': 3.7, 'Delta_Y': 22.22},
    ((0, 0, 1), 2): {'Delta_P': -31.43, 'Delta_C': -8.57, 'Delta_F': 40.0, 'Delta_X': 0.0, 'Delta_E': 0.0, 'Delta_Y': 0.0},
    ((0, 2, 3), 4): {'Delta_P': -14.4, 'Delta_C': -3.03, 'Delta_F': -6.82, 'Delta_X': -3.03, 'Delta_E': 27.27, 'Delta_Y': 0.0},
    ((0, 3, 4), 4): {'Delta_P': -10.23, 'Delta_C': -5.11, 'Delta_F': -3.41, 'Delta_X': -5.11, 'Delta_E': 23.86, 'Delta_Y': 0.0},
    ((0, 0, 4), 5): {'Delta_P': -16.67, 'Delta_C': -3.94, 'Delta_F': -1.39, 'Delta_X': 1.16, 'Delta_E': -1.39, 'Delta_Y': 22.22},
    ((0, 2, 3), 5): {'Delta_P': -15.74, 'Delta_C': -1.86, 'Delta_F': -6.48, 'Delta_X': -1.86, 'Delta_E': 3.71, 'Delta_Y': 22.22},
    ((0, 1, 2), 0): {'Delta_P': 22.23, 'Delta_C': -13.33, 'Delta_F': -8.89, 'Delta_X': 0.0, 'Delta_E': 0.0, 'Delta_Y': 0.0},
    ((0, 1, 2), 1): {'Delta_P': -17.77, 'Delta_C': 26.67, 'Delta_F': -8.89, 'Delta_X': 0.0, 'Delta_E': 0.0, 'Delta_Y': 0.0},
    ((0, 1, 2), 2): {'Delta_P': -17.77, 'Delta_C': -13.33, 'Delta_F': 31.11, 'Delta_X': 0.0, 'Delta_E': 0.0, 'Delta_Y': 0.0},
    ((0, 1, 2), 3): {'Delta_P': -16.66, 'Delta_C': -11.11, 'Delta_F': -5.55, 'Delta_X': 33.33, 'Delta_E': 0.0, 'Delta_Y': 0.0},
    ((0, 1, 2), 4): {'Delta_P': -17.17, 'Delta_C': -10.6, 'Delta_F': -4.04, 'Delta_X': 4.55, 'Delta_E': 27.27, 'Delta_Y': 0.0},
    ((0, 1, 2), 5): {'Delta_P': -18.51, 'Delta_C': -11.11, 'Delta_F': -3.7, 'Delta_X': 7.41, 'Delta_E': 3.7, 'Delta_Y': 22.22},
    ((0, 0, 2), 0): {'Delta_P': 13.33, 'Delta_C': -4.44, 'Delta_F': -8.89, 'Delta_X': 0.0, 'Delta_E': 0.0, 'Delta_Y': 0.0},
    ((0, 1, 1), 0): {'Delta_P': 26.37, 'Delta_C': -26.37, 'Delta_F': 0.0, 'Delta_X': 0.0, 'Delta_E': 0.0, 'Delta_Y': 0.0},
    ((0, 5, 5), 3): {'Delta_P': -7.4, 'Delta_C': -4.24, 'Delta_F': -3.18, 'Delta_X': 20.11, 'Delta_E': -1.05, 'Delta_Y': -4.24},
    ((0, 0, 3), 4): {'Delta_P': -21.97, 'Delta_C': -3.03, 'Delta_F': 0.76, 'Delta_X': -3.03, 'Delta_E': 27.27, 'Delta_Y': 0.0},
    ((0, 0, 2), 1): {'Delta_P': -26.67, 'Delta_C': 35.56, 'Delta_F': -8.89, 'Delta_X': 0.0, 'Delta_E': 0.0, 'Delta_Y': 0.0},
    ((0, 5, 5), 0): {'Delta_P': 14.82, 'Delta_C': -4.24, 'Delta_F': -3.18, 'Delta_X': -2.11, 'Delta_E': -1.06, 'Delta_Y': -4.24},
    ((0, 0, 5), 5): {'Delta_P': -9.53, 'Delta_C': -4.24, 'Delta_F': -3.18, 'Delta_X': -2.11, 'Delta_E': -1.06, 'Delta_Y': 20.11},
    ((0, 1, 5), 5): {'Delta_P': -7.4, 'Delta_C': -6.35, 'Delta_F': -3.18, 'Delta_X': -2.11, 'Delta_E': -1.06, 'Delta_Y': 20.11},
    ((0, 4, 5), 0): {'Delta_P': 14.82, 'Delta_C': -4.24, 'Delta_F': -3.18, 'Delta_X': -2.11, 'Delta_E': -3.18, 'Delta_Y': -2.11},
    ((0, 2, 5), 5): {'Delta_P': -7.4, 'Delta_C': -4.24, 'Delta_F': -5.29, 'Delta_X': -2.11, 'Delta_E': -1.06, 'Delta_Y': 20.11},
    ((0, 3, 5), 0): {'Delta_P': 14.82, 'Delta_C': -4.24, 'Delta_F': -3.18, 'Delta_X': -4.24, 'Delta_E': -1.06, 'Delta_Y': -2.11},
    ((0, 2, 5), 0): {'Delta_P': 14.82, 'Delta_C': -4.24, 'Delta_F': -5.29, 'Delta_X': -2.11, 'Delta_E': -1.06, 'Delta_Y': -2.11},
    ((0, 3, 5), 5): {'Delta_P': -7.4, 'Delta_C': -4.24, 'Delta_F': -3.18, 'Delta_X': -4.24, 'Delta_E': -1.06, 'Delta_Y': 20.11},
    ((0, 5, 5), 1): {'Delta_P': -7.4, 'Delta_C': 17.99, 'Delta_F': -3.18, 'Delta_X': -2.11, 'Delta_E': -1.06, 'Delta_Y': -4.24},
    ((0, 3, 4), 0): {'Delta_P': 3.24, 'Delta_C': 3.47, 'Delta_F': -1.39, 'Delta_X': -11.34, 'Delta_E': -1.39, 'Delta_Y': 7.41},
    ((0, 0, 5), 4): {'Delta_P': -9.53, 'Delta_C': -4.24, 'Delta_F': -3.18, 'Delta_X': -2.11, 'Delta_E': 21.17, 'Delta_Y': -2.11},
    ((0, 1, 4), 5): {'Delta_P': -11.57, 'Delta_C': -9.03, 'Delta_F': -1.39, 'Delta_X': 1.16, 'Delta_E': -1.39, 'Delta_Y': 22.22},
    ((0, 1, 5), 0): {'Delta_P': 14.82, 'Delta_C': -6.35, 'Delta_F': -3.18, 'Delta_X': -2.11, 'Delta_E': -1.06, 'Delta_Y': -2.11},
    ((0, 1, 5), 4): {'Delta_P': -7.4, 'Delta_C': -6.35, 'Delta_F': -3.18, 'Delta_X': -2.11, 'Delta_E': 21.17, 'Delta_Y': -2.11},
    ((0, 2, 4), 5): {'Delta_P': -11.57, 'Delta_C': -3.94, 'Delta_F': -6.48, 'Delta_X': 1.16, 'Delta_E': -1.39, 'Delta_Y': 22.22},
    ((0, 4, 5), 1): {'Delta_P': -7.4, 'Delta_C': 17.99, 'Delta_F': -3.18, 'Delta_X': -2.11, 'Delta_E': -3.18, 'Delta_Y': -2.11},
    ((0, 4, 5), 5): {'Delta_P': -7.4, 'Delta_C': -4.24, 'Delta_F': -3.18, 'Delta_X': -2.11, 'Delta_E': -3.18, 'Delta_Y': 20.11},
    ((0, 2, 4), 0): {'Delta_P': 10.65, 'Delta_C': -3.94, 'Delta_F': -13.89, 'Delta_X': 8.56, 'Delta_E': -8.8, 'Delta_Y': 7.41},
    ((0, 3, 3), 0): {'Delta_P': -0.93, 'Delta_C': -1.86, 'Delta_F': 10.19, 'Delta_X': -25.92, 'Delta_E': 3.7, 'Delta_Y': 14.81},
    ((0, 0, 4), 4): {'Delta_P': -13.64, 'Delta_C': -5.11, 'Delta_F': -3.41, 'Delta_X': -1.7, 'Delta_E': 23.86, 'Delta_Y': 0.0},
    ((0, 0, 1), 0): {'Delta_P': 13.19, 'Delta_C': -13.19, 'Delta_F': 0.0, 'Delta_X': 0.0, 'Delta_E': 0.0, 'Delta_Y': 0.0},
    ((0, 0, 3), 0): {'Delta_P': 13.89, 'Delta_C': -5.56, 'Delta_F': -2.77, 'Delta_X': -5.56, 'Delta_E': 0.0, 'Delta_Y': 0.0},
    ((0, 0, 4), 0): {'Delta_P': 13.64, 'Delta_C': -5.11, 'Delta_F': -3.41, 'Delta_X': -1.7, 'Delta_E': -3.41, 'Delta_Y': 0.0},
    ((0, 0, 5), 0): {'Delta_P': 12.7, 'Delta_C': -4.24, 'Delta_F': -3.18, 'Delta_X': -2.11, 'Delta_E': -1.06, 'Delta_Y': -2.11},
    ((0, 1, 1), 1): {'Delta_P': -19.78, 'Delta_C': 19.78, 'Delta_F': 0.0, 'Delta_X': 0.0, 'Delta_E': 0.0, 'Delta_Y': 0.0},
    ((0, 1, 1), 2): {'Delta_P': -16.19, 'Delta_C': -23.81, 'Delta_F': 40.0, 'Delta_X': 0.0, 'Delta_E': 0.0, 'Delta_Y': 0.0},
    ((0, 1, 1), 3): {'Delta_P': -15.08, 'Delta_C': -23.81, 'Delta_F': 5.56, 'Delta_X': 33.33, 'Delta_E': 0.0, 'Delta_Y': 0.0},
    ((0, 1, 1), 4): {'Delta_P': -15.59, 'Delta_C': -25.32, 'Delta_F': 9.09, 'Delta_X': 4.55, 'Delta_E': 27.27, 'Delta_Y': 0.0},
    ((0, 1, 1), 5): {'Delta_P': -16.93, 'Delta_C': -27.51, 'Delta_F': 11.11, 'Delta_X': 7.41, 'Delta_E': 3.7, 'Delta_Y': 22.22},
}

TEMPLATE_P_CANONICAL = {((0, 0, 0), 0): {'P': 53.33, 'C': 6.67, 'F': 40.0, 'X': 0.0, 'E': 0.0, 'Y': 0.0}, ((0, 4, 4), 0): {'P': 40.74, 'C': 22.22, 'F': 11.11, 'X': 7.41, 'E': 3.7, 'Y': 14.81}, ((0, 1, 4), 0): {'P': 54.55, 'C': 22.73, 'F': 9.09, 'X': 4.55, 'E': 9.09, 'Y': 0.0}, ((0, 1, 2), 0): {'P': 66.67, 'C': 20.0, 'F': 13.33, 'X': 0.0, 'E': 0.0, 'Y': 0.0}, ((0, 0, 2), 0): {'P': 80.0, 'C': 6.67, 'F': 13.33, 'X': 0.0, 'E': 0.0, 'Y': 0.0}, ((0, 1, 1), 0): {'P': 69.23, 'C': 30.77, 'F': 0.0, 'X': 0.0, 'E': 0.0, 'Y': 0.0}, ((0, 5, 5), 0): {'P': 48.15, 'C': 14.81, 'F': 11.11, 'X': 7.41, 'E': 3.7, 'Y': 14.81}, ((0, 4, 5), 0): {'P': 48.15, 'C': 14.81, 'F': 11.11, 'X': 7.41, 'E': 11.11, 'Y': 7.41}, ((0, 3, 5), 0): {'P': 48.15, 'C': 14.81, 'F': 11.11, 'X': 14.81, 'E': 3.7, 'Y': 7.41}, ((0, 2, 5), 0): {'P': 48.15, 'C': 14.81, 'F': 18.52, 'X': 7.41, 'E': 3.7, 'Y': 7.41}, ((0, 3, 4), 0): {'P': 40.74, 'C': 22.22, 'F': 11.11, 'X': 7.41, 'E': 11.11, 'Y': 7.41}, ((0, 1, 5), 0): {'P': 48.15, 'C': 22.22, 'F': 11.11, 'X': 7.41, 'E': 3.7, 'Y': 7.41}, ((0, 2, 4), 0): {'P': 48.15, 'C': 14.81, 'F': 11.11, 'X': 14.81, 'E': 3.7, 'Y': 7.41}, ((0, 3, 3), 0): {'P': 40.74, 'C': 14.81, 'F': 18.52, 'X': 7.41, 'E': 3.7, 'Y': 14.81}, ((0, 0, 1), 0): {'P': 84.62, 'C': 15.38, 'F': 0.0, 'X': 0.0, 'E': 0.0, 'Y': 0.0}, ((0, 0, 3), 0): {'P': 72.22, 'C': 11.11, 'F': 5.56, 'X': 11.11, 'E': 0.0, 'Y': 0.0}, ((0, 0, 4), 0): {'P': 63.64, 'C': 13.64, 'F': 9.09, 'X': 4.55, 'E': 9.09, 'Y': 0.0}, ((0, 0, 5), 0): {'P': 55.56, 'C': 14.81, 'F': 11.11, 'X': 7.41, 'E': 3.7, 'Y': 7.41}}

class PredictorV4:
    def __init__(self, nt_data=None, template_data=None):
        self.nt_data = nt_data or {}
        self.template_data = template_data or {}
        self.tier_order = get_canonical_tier_order()

    def predict(self, base_signature_sorted, template_dev=None):
        # Step 1: Normalize bases for NT lookup
        norm_bases, base_offset = self._normalize_bases(base_signature_sorted)
        nt_curve = self._lookup_nt_curve(norm_bases)

        # Step 2: Shift baseline curve upward by original offset (align 4-mat and NT scales)
        # This ensures template bias deltas apply on a consistent tier frame
        shifted_curve = self._shift_curve(nt_curve, base_offset)

        # Step 3: Apply template bias if template present
        if template_dev is not None:
            biased_curve = self._apply_template_bias(shifted_curve, base_signature_sorted, template_dev)
        else:
            biased_curve = shifted_curve

        # Step 4: Enforce continuous min/max bins and normalize
        final_curve = self._enforce_continuous_bins(biased_curve, base_signature_sorted, template_dev)
        return final_curve

    # ---------------- Helper methods ----------------

    def _normalize_bases(self, bases):
        min_base = min(bases)
        normalized = tuple(sorted(b - min_base for b in bases))
        return normalized, min_base

    def _lookup_nt_curve(self, normalized_bases):
        if len(normalized_bases) in self.nt_data:
            nt_map = self.nt_data[len(normalized_bases)]
            return nt_map.get(normalized_bases, {tier: 0.0 for tier in self.tier_order})
        else:
            return {tier: 0.0 for tier in self.tier_order}
        # For now, return zero distribution for structure
        return {tier: 0.0 for tier in self.tier_order}

    def _shift_curve(self, curve, offset):
        shifted = {tier: 0.0 for tier in self.tier_order}
        for i, tier in enumerate(self.tier_order):
            prob = curve[tier]
            if prob > 0:
                target_idx = i + offset
                if target_idx < len(self.tier_order):
                    shifted[self.tier_order[target_idx]] = prob
        return shifted

    def _apply_template_bias(self, curve, base_signature_sorted, template_dev):
        norm_bases = self._normalize_bases(base_signature_sorted)[0]
        key = (norm_bases, template_dev)
        if key in self.template_data:
            deltas = self.template_data[key]
            # Apply additive deltas
            adjusted = {}
            for tier in self.tier_order:
                adjusted[tier] = curve.get(tier, 0.0) + deltas.get(f'Delta_{tier}', 0.0)
            # Uniform bases shortcut: if bases are identical and template is lowest, output single tier
        if len(set(base_signature_sorted + [template_dev])) == 1:
            # 100% at lowest tier
            lowest_tier = self.tier_order[min(base_signature_sorted)]
            return {t: 100.0 if t == lowest_tier else 0.0 for t in self.tier_order}

        # If TemplateDev = 0 (P-tier template), use canonical Template-P map (bypass NT + bias)
        if template_dev == 0:
            norm_bases = self._normalize_bases(base_signature_sorted)[0]
            key = (norm_bases, 0)
            if key in TEMPLATE_P_CANONICAL:
                return TEMPLATE_P_CANONICAL[key]
            return curve

        # Apply dual-anchoring correction:
        # Compute base offset (min of bases) and global offset (min of all inputs including template)
        base_offset = min(base_signature_sorted)
        global_offset = min(base_signature_sorted + [template_dev])
        # Adjust bias application: shift relative to global offset to prevent extreme overshoot
        # (actual delta maps remain same, but applied in globally aligned frame)

        # Apply deltas if found, else fallback to direct template data (if available)
        if key in self.template_data:
            deltas = self.template_data[key]
            adjusted = {}
            for tier in self.tier_order:
                adjusted[tier] = curve.get(tier, 0.0) + deltas.get(f'Delta_{tier}', 0.0)
        else:
            # Fallback: use curve as-is (no deltas found)
            adjusted = curve

        # No clamping: negative values allowed to surface for diagnostic purposes
        adjusted = {tier: val for tier, val in adjusted.items()}

        # Enforce continuous min/max
        input_tiers = [self.tier_order[v] for v in base_signature_sorted]
        if template_dev is not None:
            input_tiers.append(self.tier_order[template_dev])
        if not validate_min_max_continuous_bins(input_tiers, adjusted):
            # Fail continuity check; return adjusted as-is (for debug/mismatch detection)
            return adjusted

        # Normalize to 100%
        total = sum(adjusted.values())
        if total > 0:
            adjusted = {k: v * (100.0 / total) for k, v in adjusted.items()}

        return adjusted
        return curve

    def _enforce_continuous_bins(self, curve, base_signature_sorted, template_dev):
        # Determine min/max from input (bases + template if present)
        input_tiers = [self.tier_order[v] for v in base_signature_sorted]
        if template_dev is not None:
            input_tiers.append(self.tier_order[template_dev])

        # Enforce continuous bins
        if not validate_min_max_continuous_bins(input_tiers, curve):
            # Fill missing bins between min and max
            min_idx = min(self.tier_order.index(t) for t in input_tiers)
            max_idx = max(self.tier_order.index(t) for t in input_tiers)
            for i in range(min_idx, max_idx + 1):
                tier = self.tier_order[i]
                if curve[tier] == 0.0:
                    curve[tier] = 0.01  # minimal filler to maintain continuity

        # Normalize to 100%
        total = sum(curve.values())
        if total > 0:
            curve = {k: v * (100.0 / total) for k, v in curve.items()}

        return curve


# Example usage
if __name__ == "__main__":
    predictor = PredictorV4()
    result = predictor.predict([1,5,5], template_dev=0)
    print(result)
