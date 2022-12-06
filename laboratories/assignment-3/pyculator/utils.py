_BASE_P = 1234577

def neg(a, P=_BASE_P):
    while a < 0:
        a += P
    return a

def add(a, b, P=_BASE_P):
    return (a + b)%P

def sub(a, b, P=_BASE_P):
    return add(a, neg(-b, P), P)

def mul(a, b, P=_BASE_P):
    return a*b % P

def div(a, b, P=_BASE_P):
    for i in range(P):
        if mul(b, i, P) == a:
            return i
    return -1

def pow(a, p, P=_BASE_P):
    if p == 0:
        return 1
    b = pow(a, p/2, P)
    b = mul(b,b, P)
    if p % 2 == 0:
        return b
    return mul(b, a, P)
