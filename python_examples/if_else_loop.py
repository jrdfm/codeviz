def process_numbers(nums):
    total = 0
    for n in nums:
        if n % 2 == 0:
            total += n
        else:
            total -= n
    return total 