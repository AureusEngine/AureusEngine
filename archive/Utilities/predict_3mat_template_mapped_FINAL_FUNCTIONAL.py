
def predict_3mat_template(recipe):
    qmap = {"P":0,"C":1,"F":2,"X":3,"E":4,"Y":5}
    tiers = ["P","C","F","X","E","Y"]

    # NT baseline map
    nt_map = {
        (0, 0, 0): [100.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        (0, 0, 1): [71.43, 28.57, 0.0, 0.0, 0.0, 0.0],
        (0, 0, 2): [66.67, 11.11, 22.22, 0.0, 0.0, 0.0],
        (0, 0, 3): [58.33, 16.67, 8.33, 16.67, 0.0, 0.0],
        (0, 0, 4): [50.0, 18.75, 12.5, 6.25, 12.5, 0.0],
        (0, 0, 5): [42.86, 19.05, 14.29, 9.52, 4.76, 9.52],
        (0, 1, 1): [42.86, 57.14, 0.0, 0.0, 0.0, 0.0],
        (0, 1, 2): [44.44, 33.33, 22.22, 0.0, 0.0, 0.0],
        (0, 1, 3): [41.67, 33.33, 8.33, 16.67, 0.0, 0.0],
        (0, 1, 4): [37.5, 31.25, 12.5, 6.25, 12.5, 0.0],
        (0, 1, 5): [33.33, 28.57, 14.29, 9.52, 4.76, 9.52],
        (0, 2, 2): [44.44, 11.11, 44.44, 0.0, 0.0, 0.0],
        (0, 2, 3): [41.67, 16.67, 25.0, 16.67, 0.0, 0.0],
        (0, 2, 4): [37.5, 18.75, 25.0, 6.25, 12.5, 0.0],
        (0, 2, 5): [33.33, 19.05, 23.81, 9.52, 4.76, 9.52],
        (0, 3, 3): [41.67, 16.67, 8.33, 33.33, 0.0, 0.0],
        (0, 3, 4): [37.5, 18.75, 12.5, 18.75, 12.5, 0.0],
        (0, 3, 5): [33.33, 19.05, 14.29, 19.05, 4.76, 9.52],
        (0, 4, 4): [37.5, 18.75, 12.5, 6.25, 25.0, 0.0],
        (0, 4, 5): [33.33, 19.05, 14.29, 9.52, 14.29, 9.52],
        (0, 5, 5): [33.33, 19.05, 14.29, 9.52, 4.76, 19.05]
    }

    # Delta parametric map
    delta_map = {
        (0, 0, 0): {'Delta_P': 0.0, 'Delta_C': 0.0, 'Delta_F': 0.0, 'Delta_X': 0.0, 'Delta_E': 0.0, 'Delta_Y': 0.0},
        (0, 0, 1): {'Delta_P': -15.87, 'Delta_C': 15.87, 'Delta_F': 0.0, 'Delta_X': 0.0, 'Delta_E': 0.0, 'Delta_Y': 0.0},
        (0, 0, 2): {'Delta_P': -12.12, 'Delta_C': -2.02, 'Delta_F': 14.14, 'Delta_X': 0.0, 'Delta_E': 0.0, 'Delta_Y': 0.0},
        (0, 0, 3): {'Delta_P': -8.33, 'Delta_C': -2.38, 'Delta_F': -1.19, 'Delta_X': 11.9, 'Delta_E': 0.0, 'Delta_Y': 0.0},
        (0, 0, 4): {'Delta_P': -5.56, 'Delta_C': -2.08, 'Delta_F': -1.39, 'Delta_X': -0.69, 'Delta_E': 9.72, 'Delta_Y': 0.0},
        (0, 0, 5): {'Delta_P': -3.73, 'Delta_C': -1.66, 'Delta_F': -1.25, 'Delta_X': -0.82, 'Delta_E': -0.41, 'Delta_Y': 7.87},
        (0, 1, 0): {'Delta_P': 6.35, 'Delta_C': -6.35, 'Delta_F': 0.0, 'Delta_X': 0.0, 'Delta_E': 0.0, 'Delta_Y': 0.0},
        (0, 1, 1): {'Delta_P': -9.53, 'Delta_C': 9.53, 'Delta_F': 0.0, 'Delta_X': 0.0, 'Delta_E': 0.0, 'Delta_Y': 0.0},
        (0, 1, 2): {'Delta_P': -8.08, 'Delta_C': -6.06, 'Delta_F': 14.14, 'Delta_X': 0.0, 'Delta_E': 0.0, 'Delta_Y': 0.0},
        (0, 1, 3): {'Delta_P': -5.96, 'Delta_C': -4.76, 'Delta_F': -1.19, 'Delta_X': 11.9, 'Delta_E': 0.0, 'Delta_Y': 0.0},
        (0, 1, 4): {'Delta_P': -4.17, 'Delta_C': -3.47, 'Delta_F': -1.39, 'Delta_X': -0.69, 'Delta_E': 9.72, 'Delta_Y': 0.0},
        (0, 1, 5): {'Delta_P': -2.9, 'Delta_C': -2.48, 'Delta_F': -1.25, 'Delta_X': -0.82, 'Delta_E': -0.41, 'Delta_Y': 7.87},
        (0, 2, 0): {'Delta_P': 6.06, 'Delta_C': -2.02, 'Delta_F': -4.04, 'Delta_X': 0.0, 'Delta_E': 0.0, 'Delta_Y': 0.0},
        (0, 2, 1): {'Delta_P': -8.08, 'Delta_C': 12.12, 'Delta_F': -4.04, 'Delta_X': 0.0, 'Delta_E': 0.0, 'Delta_Y': 0.0},
        (0, 2, 2): {'Delta_P': -8.08, 'Delta_C': -2.02, 'Delta_F': 10.11, 'Delta_X': 0.0, 'Delta_E': 0.0, 'Delta_Y': 0.0},
        (0, 2, 3): {'Delta_P': -5.96, 'Delta_C': -2.38, 'Delta_F': -3.57, 'Delta_X': 11.9, 'Delta_E': 0.0, 'Delta_Y': 0.0},
        (0, 2, 4): {'Delta_P': -4.17, 'Delta_C': -2.08, 'Delta_F': -2.78, 'Delta_X': -0.69, 'Delta_E': 9.72, 'Delta_Y': 0.0},
        (0, 2, 5): {'Delta_P': -2.9, 'Delta_C': -1.66, 'Delta_F': -2.07, 'Delta_X': -0.82, 'Delta_E': -0.41, 'Delta_Y': 7.87},
        (0, 3, 0): {'Delta_P': 5.96, 'Delta_C': -2.38, 'Delta_F': -1.19, 'Delta_X': -2.38, 'Delta_E': 0.0, 'Delta_Y': 0.0},
        (0, 3, 1): {'Delta_P': -5.96, 'Delta_C': 9.53, 'Delta_F': -1.19, 'Delta_X': -2.38, 'Delta_E': 0.0, 'Delta_Y': 0.0},
        (0, 3, 2): {'Delta_P': -5.96, 'Delta_C': -2.38, 'Delta_F': 10.71, 'Delta_X': -2.38, 'Delta_E': 0.0, 'Delta_Y': 0.0},
        (0, 3, 3): {'Delta_P': -5.96, 'Delta_C': -2.38, 'Delta_F': -1.19, 'Delta_X': 9.53, 'Delta_E': 0.0, 'Delta_Y': 0.0},
        (0, 3, 4): {'Delta_P': -4.17, 'Delta_C': -2.08, 'Delta_F': -1.39, 'Delta_X': -2.08, 'Delta_E': 9.72, 'Delta_Y': 0.0},
        (0, 3, 5): {'Delta_P': -2.9, 'Delta_C': -1.66, 'Delta_F': -1.25, 'Delta_X': -1.66, 'Delta_E': -0.41, 'Delta_Y': 7.87},
        (0, 4, 0): {'Delta_P': 5.56, 'Delta_C': -2.08, 'Delta_F': -1.39, 'Delta_X': -0.69, 'Delta_E': -1.39, 'Delta_Y': 0.0},
        (0, 4, 1): {'Delta_P': -4.17, 'Delta_C': 7.64, 'Delta_F': -1.39, 'Delta_X': -0.69, 'Delta_E': -1.39, 'Delta_Y': 0.0},
        (0, 4, 2): {'Delta_P': -4.17, 'Delta_C': -2.08, 'Delta_F': 8.33, 'Delta_X': -0.69, 'Delta_E': -1.39, 'Delta_Y': 0.0},
        (0, 4, 3): {'Delta_P': -4.17, 'Delta_C': -2.08, 'Delta_F': -1.39, 'Delta_X': 9.03, 'Delta_E': -1.39, 'Delta_Y': 0.0},
        (0, 4, 4): {'Delta_P': -4.17, 'Delta_C': -2.08, 'Delta_F': -1.39, 'Delta_X': -0.69, 'Delta_E': 8.33, 'Delta_Y': 0.0},
        (0, 4, 5): {'Delta_P': -2.9, 'Delta_C': -1.66, 'Delta_F': -1.25, 'Delta_X': -0.82, 'Delta_E': -1.25, 'Delta_Y': 7.87},
        (0, 5, 0): {'Delta_P': 4.97, 'Delta_C': -1.66, 'Delta_F': -1.25, 'Delta_X': -0.82, 'Delta_E': -0.41, 'Delta_Y': -0.82},
        (0, 5, 1): {'Delta_P': -2.9, 'Delta_C': 6.21, 'Delta_F': -1.25, 'Delta_X': -0.82, 'Delta_E': -0.41, 'Delta_Y': -0.82},
        (0, 5, 2): {'Delta_P': -2.9, 'Delta_C': -1.66, 'Delta_F': 6.62, 'Delta_X': -0.82, 'Delta_E': -0.41, 'Delta_Y': -0.82},
        (0, 5, 3): {'Delta_P': -2.9, 'Delta_C': -1.66, 'Delta_F': -1.25, 'Delta_X': 7.04, 'Delta_E': -0.41, 'Delta_Y': -0.82},
        (0, 5, 4): {'Delta_P': -2.9, 'Delta_C': -1.66, 'Delta_F': -1.25, 'Delta_X': -0.82, 'Delta_E': 7.45, 'Delta_Y': -0.82},
        (0, 5, 5): {'Delta_P': -2.9, 'Delta_C': -1.66, 'Delta_F': -1.25, 'Delta_X': -0.82, 'Delta_E': -0.41, 'Delta_Y': 7.04},
        (1, 1, 0): {'Delta_P': 12.7, 'Delta_C': -12.7, 'Delta_F': 0.0, 'Delta_X': 0.0, 'Delta_E': 0.0, 'Delta_Y': 0.0},
        (1, 2, 0): {'Delta_P': 10.11, 'Delta_C': -6.06, 'Delta_F': -4.04, 'Delta_X': 0.0, 'Delta_E': 0.0, 'Delta_Y': 0.0},
        (1, 3, 0): {'Delta_P': 8.33, 'Delta_C': -4.76, 'Delta_F': -1.19, 'Delta_X': -2.38, 'Delta_E': 0.0, 'Delta_Y': 0.0},
        (1, 4, 0): {'Delta_P': 6.94, 'Delta_C': -3.47, 'Delta_F': -1.39, 'Delta_X': -0.69, 'Delta_E': -1.39, 'Delta_Y': 0.0},
        (1, 5, 0): {'Delta_P': 5.8, 'Delta_C': -2.48, 'Delta_F': -1.25, 'Delta_X': -0.82, 'Delta_E': -0.41, 'Delta_Y': -0.82},
        (2, 2, 0): {'Delta_P': 10.11, 'Delta_C': -2.02, 'Delta_F': -8.08, 'Delta_X': 0.0, 'Delta_E': 0.0, 'Delta_Y': 0.0},
        (2, 3, 0): {'Delta_P': 8.33, 'Delta_C': -2.38, 'Delta_F': -3.57, 'Delta_X': -2.38, 'Delta_E': 0.0, 'Delta_Y': 0.0},
        (2, 4, 0): {'Delta_P': 6.94, 'Delta_C': -2.08, 'Delta_F': -2.78, 'Delta_X': -0.69, 'Delta_E': -1.39, 'Delta_Y': 0.0},
        (2, 5, 0): {'Delta_P': 5.8, 'Delta_C': -1.66, 'Delta_F': -2.07, 'Delta_X': -0.82, 'Delta_E': -0.41, 'Delta_Y': -0.82},
        (3, 3, 0): {'Delta_P': 8.33, 'Delta_C': -2.38, 'Delta_F': -1.19, 'Delta_X': -4.76, 'Delta_E': 0.0, 'Delta_Y': 0.0},
        (3, 5, 0): {'Delta_P': 5.8, 'Delta_C': -1.66, 'Delta_F': -1.25, 'Delta_X': -1.66, 'Delta_E': -0.41, 'Delta_Y': -0.82},
        (3, 4, 0): {'Delta_P': 6.94, 'Delta_C': -2.08, 'Delta_F': -1.39, 'Delta_X': -2.08, 'Delta_E': -1.39, 'Delta_Y': 0.0},
        (4, 4, 0): {'Delta_P': 6.94, 'Delta_C': -2.08, 'Delta_F': -1.39, 'Delta_X': -0.69, 'Delta_E': -2.78, 'Delta_Y': 0.0},
        (4, 5, 0): {'Delta_P': 5.8, 'Delta_C': -1.66, 'Delta_F': -1.25, 'Delta_X': -0.82, 'Delta_E': -1.25, 'Delta_Y': -0.82},
        (5, 5, 0): {'Delta_P': 5.8, 'Delta_C': -1.66, 'Delta_F': -1.25, 'Delta_X': -0.82, 'Delta_E': -0.41, 'Delta_Y': -1.66}
    }

    devs = [qmap[ch] for ch in recipe]
    min_dev = min(devs)
    max_dev = max(devs)

    # Normalize
    norm = [d - min_dev for d in devs]

    # Get NT baseline
    nt_key = tuple(sorted(norm))
    if nt_key not in nt_map:
        return None
    nt_bins = nt_map[nt_key]

    # Get delta
    min_b, max_b = sorted(norm[:2])
    t_dev = norm[2]
    delta = delta_map.get((min_b, max_b, t_dev))
    if delta is None:
        return None

    predicted = [
        round(nt_bins[0] + delta['Delta_P'], 2),
        round(nt_bins[1] + delta['Delta_C'], 2),
        round(nt_bins[2] + delta['Delta_F'], 2),
        round(nt_bins[3] + delta['Delta_X'], 2),
        round(nt_bins[4] + delta['Delta_E'], 2),
        round(nt_bins[5] + delta['Delta_Y'], 2)
    ]

    # Map normalized bins to actual min..max tiers
    spread = max_dev - min_dev
    mapped_bins = {}
    for i, prob in enumerate(predicted):
        tier_index = min_dev + i
        if tier_index > max_dev:
            break
        mapped_bins[tiers[tier_index]] = prob

    return mapped_bins
