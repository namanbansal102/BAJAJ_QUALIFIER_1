from functools import reduce
import math

def generate_fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib

def filter_primes(numbers):
    def is_prime(n):
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True
    return [num for num in numbers if is_prime(num)]

def calculate_lcm(numbers):
    def lcm_two(a, b):
        return abs(a * b) // math.gcd(a, b)
    return reduce(lcm_two, numbers)

def calculate_hcf(numbers):
    return reduce(math.gcd, numbers)
