import subprocess
import sys
import time
from math import gcd

from sympy import factorint, integer_nthroot

from cubefull_count import count


def oeis_program(n):
    m, c = 10 ** n, 0
    for x in range(1, integer_nthroot(m, 5)[0] + 1):
        if all(d <= 1 for d in factorint(x).values()):
            for y in range(1, integer_nthroot(z := m // x ** 5, 4)[0] + 1):
                if gcd(x, y) == 1 and all(d <= 1 for d in factorint(y).values()):
                    c += integer_nthroot(z // y ** 4, 3)[0]
    return c


def timed(f, *a):
    t = time.perf_counter()
    r = f(*a)
    return r, time.perf_counter() - t


binary = sys.argv[1] if len(sys.argv) > 1 else None
print("n, OEIS python program, this python, this C")
for n in (8, 12, 16, 20, 22, 24, 26):
    v1, t1 = timed(oeis_program, n)
    v2, t2 = timed(count, 10 ** n)
    assert v1 == v2
    t3 = ""
    if binary:
        out = subprocess.run([binary, str(10 ** n)], capture_output=True, text=True).stdout
        t3 = out.split("time=")[1].split("s")[0]
    print(n, round(t1, 3), round(t2, 4), t3, flush=True)
for n in (28, 32):
    v2, t2 = timed(count, 10 ** n)
    t3 = ""
    if binary:
        out = subprocess.run([binary, str(10 ** n)], capture_output=True, text=True).stdout
        t3 = out.split("time=")[1].split("s")[0]
    print(n, "-", round(t2, 3), t3, v2, flush=True)
