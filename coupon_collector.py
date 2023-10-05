import functools
import math
from fractions import Fraction

@functools.cache
def C(n, k):
    return math.comb(n, k)

# Expected values
def ev_subset(s, m=1):
    """E(N) for N draws of m-subsets to cover s coupons."""
    return -sum(Fraction((-1) ** k * C(s, k),
                         1 - Fraction(C(s - k, m), C(s, m)))
                for k in range(1, s + 1))

def ev_replace(s, m=1):
    """E(N) for N draws of m-packs to cover s coupons."""
    return -sum(Fraction((-1) ** k * C(s, k),
                         1 - Fraction(pow(s - k, m), pow(s, m)))
                for k in range(1, s + 1))

# Cumulative distributions
def p_subset(n, s, m=1):
    """P(N<=n) for N draws of m-subsets to cover s coupons."""
    return Fraction(sum((-1) ** k * C(s, k) * pow(C(s - k, m), n)
                        for k in range(0, s + 1)),
                    pow(C(s, m), n))

def p_replace(n, s, m=1):
    """P(N<=n) for N draws of m-packs to cover s coupons."""
    return Fraction(sum((-1) ** k * C(s, k) * pow(s - k, m * n)
                        for k in range(0, s + 1)),
                    pow(s, m * n))

def p_interval(n, s, m=1):
    """P(N<=n) for N draws of m-intervals to cover cycle of s coupons."""
    return Fraction(sum(Fraction(s, j) * distinct(j, n) * cover(j, s, m)
                        for j in range(1, n + 1)),
                    pow(s, n))

def distinct(j, n):
    """Ways to select exactly j given distinct intervals in n draws."""
    return sum((-1) ** k * C(j, k) * pow(j - k, n)
               for k in range(0, j))

@functools.cache
def cover(j, s, m):
    """Ways to cover cycle of s coupons with j distinct m-intervals."""
    return sum((-1) ** k * C(j, k) * C(s - 1 - k * m, j - 1)
               for k in range(0, (s - j) // m + 1))

if __name__ == '__main__':
    print(sum(float(1 - p_interval(n, 1000, 10)) for n in range(1500, -1, -1)))
