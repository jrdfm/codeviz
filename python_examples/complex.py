def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None

class DataProcessor:
    def __init__(self, data):
        self.data = data
    def squared(self):
        return [x**2 for x in self.data if x > 0]
    def mean(self):
        if not self.data:
            return None
        return sum(self.data) / len(self.data) 