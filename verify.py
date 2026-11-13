import random
import subprocess
import sys

import sympy

from cubefull_count import brute, count, pair_count, triple_count

oeis = [1, 2, 7, 20, 51, 129, 307, 713, 1645, 3721, 8348, 18589, 41136, 90619, 198767, 434572, 947753, 2062437, 4480253, 9718457, 21055958, 45575049, 98566055, 213028539, 460160083, 993533517, 2144335391, 4626664451, 9980028172, 21523027285, 46408635232, 100053270534]
x = sympy.symbols("x")
local = sympy.cancel((1 - x + x ** 3) * (1 - x ** 3) * (1 - x ** 4) * (1 - x ** 5) / (1 - x))
assert sympy.expand(local - (1 - x ** 8 - x ** 9 - x ** 10 + x ** 13 + x ** 14)) == 0
for n in range(0, 25):
    assert count(10 ** n) == oeis[n], n
for m in list(range(1, 400)) + [4321, 20000, 99999, 300000]:
    assert count(m) == brute(m), m
random.seed(5)
for z in [random.randint(1, 10 ** 6) for _ in range(200)]:
    direct = sum(1 for b in range(1, 100) for a in range(1, 200) if a ** 3 * b ** 4 <= z)
    assert pair_count(z) == direct, z
for y in [random.randint(1, 10 ** 5) for _ in range(100)]:
    direct = sum(1 for c in range(1, 20) for b in range(1, 40) for a in range(1, 50) if a ** 3 * b ** 4 * c ** 5 <= y)
    assert triple_count(y) == direct, y
if len(sys.argv) > 1:
    binary = sys.argv[1]
    for n in list(range(0, 27)):
        out = subprocess.run([binary, str(10 ** n)], capture_output=True, text=True, check=True).stdout.split()[0]
        assert int(out) == oeis[n], n
    for m in [random.randint(1, 10 ** 15) for _ in range(30)] + [2 ** 60, 3 ** 40, 7 ** 30, 10 ** 20 + 12345]:
        out = subprocess.run([binary, str(m)], capture_output=True, text=True, check=True).stdout.split()[0]
        assert int(out) == count(m), m
print("ok")
