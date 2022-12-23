import random
from decimal import Decimal
import numpy as np

TIIKI = 10**3


def reconstruct_secret(shares):
    sums = 0
    for j, share_j in enumerate(shares):
        xj, yj = share_j
        prod = Decimal(1)
        for i, share_i in enumerate(shares):
            xi, _ = share_i
            if i != j:
                prod *= Decimal(Decimal(xi)/(xi-xj))
        prod *= yj
        sums += Decimal(prod)
    return int(round(Decimal(sums), 0))


def polynom(x, ci):
    point = 0
    for cIndex, cv in enumerate(ci[::-1]):
        v = x ** cIndex * cv
        point += v
    return point


def coeff(t, secret):
    coeff = [random.randrange(0, TIIKI) for _ in range(t - 1)]
    coeff.append(secret)
    return coeff


def calc_shares(n, m, secret):
    ci = coeff(m, secret)
    r = tuple(ci)
    print(f'r: {r}')
    shares = []
    for i in range(1, n+1):
        x = random.randrange(1, TIIKI)
        shares.append((x, polynom(x, ci)))
    return shares

t, n = 2,3
print(f'(t,n): {t},{n}')
secret = 777
print(f'秘密情報: {secret}')
shares = calc_shares(n, t, secret)
m = np.array((tuple(map(lambda x: (x[0], 1), shares))))
print(f'm: {m}')
s = tuple(map(lambda x: x[1], shares))
print(f's: {s}')
pool = random.sample(shares, t)
print(f'計算した秘密情報: {reconstruct_secret(pool)}')
