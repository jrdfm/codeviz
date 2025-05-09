# Function with docstring and default argument
def greet(name, greeting="Hello"):
    """Return a greeting message."""
    return f"{greeting}, {name}!"

# Class with a method
class Counter:
    def __init__(self):
        self.value = 0
    def increment(self):
        self.value += 1

# For loop and if statement
def sum_even(numbers):
    total = 0
    for n in numbers:
        if n % 2 == 0:
            total += n
    return total
