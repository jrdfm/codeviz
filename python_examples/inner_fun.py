# inner function example

def outer_function(x):
    def inner_function1(z):
        return x + z
    def inner_function2(y):
        return x + y
    return inner_function1 if x > 0 else inner_function2

result = outer_function(10)(20)
print(result)



