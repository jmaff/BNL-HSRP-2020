import math
import decimal


# h/k decoding algorithm - a and b can be functions, or a can be a list while b is a function (for finite simple CFs)
def hk_gen_decode(a, b, n):
    h = [0, 1]
    k = [1, 0]

    for i in range(0, n):
        if callable(a) and callable(b):
            h.append(a(i) * h[i - 1 + 2] + b(i - 1) * h[i - 2 + 2])
            k.append(a(i) * k[i - 1 + 2] + b(i - 1) * k[i - 2 + 2])
        elif type(a) is list and callable(b):
            h.append(a[i] * h[i - 1 + 2] + b(i - 1) * h[i - 2 + 2])
            k.append(a[i] * k[i - 1 + 2] + b(i - 1) * k[i - 2 + 2])
        else:
            raise TypeError("Incompatible parameter type for a and/or b")

    return h[len(h)-1], k[len(k)-1]


# h/k decoding algorithm for generalized cfs of the "pi" form
def hk_quadlin_gen_decode(a0, b0, coeff, n):
    def a(i): return a0 if i == 0 else coeff[3]*i+coeff[4]

    def b(i):
        return 1 if i == -1 else b0 if i == 0 else coeff[0]*i**2+coeff[1]*i+coeff[2]

    return hk_gen_decode(a, b, n)


# h/k decoding algorithm for simple CFs (a can be a list or function (if function, n is required))
def hk_simple_decode(a, n=None):
    if n is None:
        if type(a) is list:
            return hk_gen_decode(a, lambda i: 1, len(a))
        else:
            raise TypeError("n must be provided if a is not of type List")
    else:
        return hk_gen_decode(a, lambda i: 1, n)


# converts a fractional decoded CF to high-precision decimal
def hk_decode_to_decimal(decoded, precision=1025):
    decimal.getcontext().prec = precision
    dec = decimal.Decimal
    return dec(decoded[0]) / dec(decoded[1])


# simple CF encoding algorithm
def simple_encode(x, max_terms, epsilon=1e-9):
    terms = []

    while len(terms) < max_terms:
        terms.append(math.floor(x))
        x = x - math.floor(x)
        if x < epsilon:
            break
        x = 1 / x
    return terms


# find the longest repeated subsequence of a cf (or any list)
def lrss(seq):
    def match(seq1, seq2):
        result = []
        for i in range(min(len(seq1), len(seq2))):
            if seq1[i] == seq2[i]:
                result.append(seq1[i])
            else:
                break
        return result

    suffixes = [seq[i:len(seq)] for i in range(len(seq))]
    suffixes.sort()

    longest = []
    for i in range(len(suffixes)-1):
        candidate = match(suffixes[i], suffixes[i+1])

        if len(candidate) > len(longest):
            longest = candidate
    return longest
