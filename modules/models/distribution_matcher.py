
from collections import defaultdict

class DistributionMatcher:
    def __init__(self):
        self.templates = defaultdict(list)

    def add_template(self, materials, distribution):
        key = tuple(sorted(materials))
        self.templates[key].append(distribution)

    def match_distribution(self, materials):
        key = tuple(sorted(materials))
        return self.templates.get(key, [])
