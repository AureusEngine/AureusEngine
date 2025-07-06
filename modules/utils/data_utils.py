
# Utility functions for data transformation and processing

def normalize_distribution(distribution):
    total = sum(distribution)
    if total == 0:
        return [0] * len(distribution)
    return [round(val / total, 6) for val in distribution]

def average_distributions(distributions):
    if not distributions:
        return []
    length = len(distributions[0])
    summed = [sum(d[i] for d in distributions) for i in range(length)]
    return normalize_distribution(summed)
