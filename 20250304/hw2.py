def gcd(a: int, b: int) -> int:
    if b == 0:
        return a
    return gcd(b, a % b)

x, y = 7, 49
print(f"GCD of {x} and {y} is {gcd(x, y)}")
x, y = 11, 121
print(f"GCD of {x} and {y} is {gcd(x, y)}")