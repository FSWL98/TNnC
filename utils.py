import math
import numpy as np


def get_S(p):
    res = []
    S = 2
    N = get_N(p, S)

    while N < 20000000:
        res.append(S)
        S += 1
        N = get_N(p, S)

    return res


def get_N(p, S):
    return p ** S - 1


def get_m(s):
    res = []
    i = 1
    while i <= math.sqrt(s):
        if s % i == 0:
            if s / i == i:
                res.append(int(i))
            else:
                res.append(int(i))
                res.append(int(s / i))
        i += 1

    if s not in res:
        res.append(s)
    
    return sorted(res)

def get_r(p, m):
    r = []
    pwr = p ** m - 1
    # print(f'{p=} {m=}')
    for a in range(1, pwr):
        if math.gcd(a, pwr) == 1:
            linked = get_linked_elements(a, p, m)
            # print(*linked, sep='  ')
            if min(linked) == a:
                a_p = to_base(a, p)
                r.append((a, a_p, get_g(a_p, p)))
    return r


def get_g(n, p):
    return sum(int(i, p) for i in str(n))


def to_base(n, base):
    return np.base_repr(n, base=base)


def get_C1(r, p, s, m):
    calc_c = (lambda r, i, k: r + i * k) if p == 2 else (lambda r, i, k: r + 2 * i * k)
    k = (p ** m - 1)
    N = (p ** s - 1)
    l = N // k + 1

    res = []

    for i in range(l + 1):
        C = calc_c(r, i, k)

        if C > N:
            C = C % l

        C_p = to_base(C, p)
        g_c = get_g(C_p, p)

        r_p = to_base(r, p)
        g_r = get_g(r_p, p)

        if g_c == g_r:
            C2 = get_C2(C, p, s)
            # yield C, C_p, g_c, C2
            res.append((C, C_p, g_c, C2))

        if C == r and i != 0:
            break

    return res


def get_C2(c, p, s):
    linked = get_linked_elements(c, p, s)

    return min(linked)


def get_linked_elements(a, p, b):
    linked_elements = [a]
    n = a
    for _ in range(b - 1):
        n = n * p % (p ** b - 1)
        linked_elements.append(n)

    return linked_elements





if __name__ == '__main__':
    R = to_base(17, 3)
    print(R)