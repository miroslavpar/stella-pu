class Flow:
    def __init__(self, rate):
        self.rate = rate

    def apply(self, stock):
        stock.update_value(self.rate)
