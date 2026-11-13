from math import isqrt


def iroot(n, k):
    if n < 2:
        return n
    if k == 2:
        return isqrt(n)
    r = int(round(n ** (1.0 / k)))
    while r ** k > n:
        r -= 1
    while (r + 1) ** k <= n:
        r += 1
    return r


def primes_upto(m):
    if m < 2:
        return []
    sieve = bytearray([1]) * (m + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, isqrt(m) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
    return [i for i in range(m + 1) if sieve[i]]


RHO = {8: -1, 9: -1, 10: -1, 13: 1, 14: 1}


def support_terms(x):
    primes = primes_upto(iroot(x, 8))
    terms = [(1, 1)]

    def walk(start, t, w):
        for k in range(start, len(primes)):
            p = primes[k]
            base = t * p ** 8
            if base > x:
                break
            for e, c in RHO.items():
                q = t * p ** e
                if q <= x:
                    terms.append((q, w * c))
                    walk(k + 1, q, w * c)

    walk(0, 1, 1)
    return terms


def pair_count(z):
    if z < 1:
        return 0
    a_max = iroot(z, 7)
    total = -a_max * a_max
    for a in range(1, a_max + 1):
        total += iroot(z // a ** 3, 4)
        total += iroot(z // a ** 4, 3)
    return total


def triple_count(y):
    return sum(pair_count(y // c ** 5) for c in range(1, iroot(y, 5) + 1))


def count(x):
    if x < 1:
        return 0
    return sum(w * triple_count(x // r) for r, w in support_terms(x))


def brute(x):
    def cubefull(n):
        m = n
        p = 2
        while p * p * p <= m:
            if m % p == 0:
                e = 0
                while m % p == 0:
                    m //= p
                    e += 1
                if e < 3:
                    return False
            p += 1
        return m == 1
    return sum(1 for n in range(1, x + 1) if cubefull(n))
