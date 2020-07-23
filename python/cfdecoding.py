# Simple CF decoding using the h/k algorithm
max_terms = 7

cf = [14, 7, 2, 2, 1, 2, 1, 1, 1, 12, 23, 1, 1, 1, 4, 1, 16, 1, 33, 4]  # CF encoding of zeta zero 1 from cfencoding.py

# TODO: Refactor to not initialize array
h = [0 for _ in range(max_terms+2)]
k = [0 for _ in range(max_terms+2)]

if len(cf) == 0:
    raise ValueError("Error - missing cf data!")

h[0] = 0
k[0] = 1
h[1] = 1
k[1] = 0

print(f"Using {max_terms} terms, the continued fraction expansion is:")
print(f"{'a':>5}{'h':>15}{'k':>15}{'convergent':>20}")

for n in range(2, max_terms+2):
    a = cf[n-2]

    h[n] = a*h[n-1]+h[n-2]
    k[n] = a*k[n-1]+k[n-2]

    convergent = h[n] / k[n]

    print(f"{a:>5.0f}{h[n]:>15}{k[n]:>15}{convergent:>20.14f}")
