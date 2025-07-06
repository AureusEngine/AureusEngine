class LossZoneMonitor:
    def __init__(self):
        self.loss_windows = []
        self.history = []
        self.thresholds = [(0.75, 10, 0.6), (0.80, 20, 0.8), (0.90, 30, 0.95)]
        self.decay = 0.95

    def update(self, pattern_history):
        self.history = pattern_history[-100:]  # keep recent history
        self.loss_windows = self.detect_zones()

    def detect_zones(self):
        zones = []
        for conf_thresh, count, ratio in self.thresholds:
            window = self.history[-count:]
            if len(window) == count:
                losses = window.count("L")
                if losses / count >= ratio:
                    zones.append((conf_thresh, count, ratio))
        return zones

    def is_loss_zone(self):
        return len(self.loss_windows) > 0