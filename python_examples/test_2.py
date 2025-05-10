numbers = [1, 2, 3, 4, 5]
squared = [n ** 2 for n in numbers]

for num in squared:
    if num % 2 == 0:
        print(num) 
    else:
        print("odd")


x = 10
y = 20
z = 30


print("x is greater than y") if x > y else print("y is greater than x")
