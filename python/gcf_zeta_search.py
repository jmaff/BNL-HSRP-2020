import cf
import decimal
import itertools
import time

zeta_zeros = []

def load_zeros():
    with open('ZetaZeroes1024.txt', 'r') as f:
        for line in f:
            if line == '\n' or line == '  \n':
                zeta_zeros.append('')
            else:
                zeta_zeros[len(zeta_zeros) - 1] += line.strip()
    zeta_zeros.pop()


def gcf_search(n):
    decimal.getcontext().prec = 1025
    dec = decimal.Decimal

    zero = dec(zeta_zeros[n])
    initial_terms = [1, 2, 3, 5, 7, 11, 13, 17, 19]
    coeffs = [-19, -17, -13, -11, -7, -5, -3, -2, -1, 0, 1, 2, 3, 5, 7, 11, 13, 17, 19]

    min_delta = 10000

    print(f"{'a0':^5}{'b0':^5}{'A':^5}{'B':^5}{'C':^5}{'D':^5}{'E':^5}{'delta':^15}")
    for a0, b0 in itertools.product(initial_terms, initial_terms):
        for a, b, c, d, e in itertools.product(coeffs, coeffs, coeffs, coeffs, coeffs):
            convergent = cf.hk_quadlin_gen_decode(a0, b0, [a, b, c, d, e], 15, zero)

            if convergent is not None:
                delta = zero - cf.hk_decode_to_decimal(convergent)
                if abs(delta) < min_delta:
                    print(f"{a0:^5}{b0:^5}{a:^5}{b:^5}{c:^5}{d:^5}{e:^5}{delta:^15.8e}")
                    write_progress(a0, b0, a, b, c, d, e, f"{delta:.8e}")
                    min_delta = abs(delta)


def write_progress(a0, b0, a, b, c, d, e, delta):
    with open('gcf-search-progress.txt', 'a') as f:
        f.write(f"a0:{a0} b0:{b0} A:{a} B:{b} C:{c} D:{d} E:{e} Delta:{delta}\n")


start = 5
end = 10
load_zeros()
start_time = time.time()

open('gcf-search-progress.txt', 'w').close()

for i in range(start, end + 1):
    with open('gcf-search-progress.txt', 'a') as f:
        f.write(f"*****Zero #{i}*****\n")
    print("*****************************")
    print(f"Zero #{i}")
    print("*****************************")
    gcf_search(i)

print(f"Time elapsed: { time.time() - start_time } seconds")
