import random
from decimal import Decimal

TIIKI = 10**5


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
        point += x ** cIndex * cv
    return point


def coeff(t, secret):
    coeff = [random.randrange(0, TIIKI) for _ in range(t - 1)]
    coeff.append(secret)
    return coeff


def calc_shares(n, m, secret):
    ci = coeff(m, secret)
    print(f't-1次多項式f(x) [暗号化]: {ci}')
    shares = []
    for i in range(1, n+1):
        x = random.randrange(1, TIIKI)
        shares.append((x, polynom(x, ci)))
    return shares

t, n = 3, 5
print(f'(t,n): {t},{n}')
secret = 777
print(f'秘密情報: {secret}')
shares = calc_shares(n, t, secret)
print(f'シェアの集合: {", ".join(str(share) for share in shares)}')
pool = random.sample(shares, t)
print(f'復元するため選んだ集合: {", ".join(str(share) for share in pool)}')
print(f'計算した秘密情報: {reconstruct_secret(pool)}')
