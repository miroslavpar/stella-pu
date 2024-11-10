class Stock:
    def __init__(self, name, initial_value):
        self.name = name
        self.value = initial_value

    def update_value(self, change):
        self.value += change
