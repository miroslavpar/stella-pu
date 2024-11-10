class StatusIndicator:
    def __init__(self, min_val, max_val):
        self.min_val = min_val
        self.max_val = max_val

    def check_status(self, value):
        if value < self.min_val:
            return "yellow"
        elif self.min_val <= value <= self.max_val:
            return "green"
        else:
            return "red"
