def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b

# Function with if-elif-else

def sign(x):
    if x > 0:
        return "positive"
    elif x < 0:
        return "negative"
    else:
        return "zero"

# Function with boolean operations

def is_teenager(age):
    return age >= 13 and age <= 19

# Function with a while loop

def countdown(n):
    result = []
    while n > 0:
        result.append(n)
        n -= 1
    return result

# Function with try-except-finally

def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None
    finally:
        print("Division attempted.")









