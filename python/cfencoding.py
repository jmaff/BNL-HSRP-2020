# Simple cf encoding using the algorithm from the slide deck
import math


def encode_cf(x):
    terms = []
    while len(terms) < 20:
        terms.append(math.floor(x))
        x = x-math.floor(x)
        if x < 1e-9:
            break
        x = 1/x
    return terms


num = 14.1347251417346937904572519835625

result = encode_cf(num)
print(f"To {len(result)} terms, the simple continued fraction for {num} is")
print(result)
