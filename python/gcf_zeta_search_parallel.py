import cf
import decimal
import itertools
import time
from multiprocessing import Pool

zeta_zeros_global = []


def load_zeros():
    with open('ZetaZeroes1024.txt', 'r') as f:
        for line in f:
            if line == '\n' or line == '  \n':
                zeta_zeros_global.append('')
            else:
                zeta_zeros_global[len(zeta_zeros_global) - 1] += line.strip()
    zeta_zeros_global.pop()


def gcf_search(n, initial_terms, zeta_zeros):
    decimal.getcontext().prec = 1025
    dec = decimal.Decimal

    zero = dec(zeta_zeros[n])
    coeffs = [-19, -17, -13, -11, -7, -5, -3, -2, -1, 0, 1, 2, 3, 5, 7, 11, 13, 17, 19]
    initial_terms_full = [1, 2, 3, 5, 7, 11, 13, 17, 19]

    min_delta = 10000

    best_fit = [0, 0, 0, 0, 0, 0, 0, 0]

    for a0, b0 in itertools.product(initial_terms, initial_terms_full):
        for a, b in itertools.product(coeffs, coeffs):
            # if a != 0:
            #     if not (a > 0 and b >= -2 * a) and not (a < 0 and b <= -2 * a):
            #         continue
            for c, d, e in itertools.product(coeffs, coeffs, coeffs):
                convergent = cf.hk_quadlin_gen_decode(a0, b0, [a, b, c, d, e], 15, zero)

                if convergent is not None:
                    delta = zero - cf.hk_decode_to_decimal(convergent)
                    if abs(delta) < min_delta:
                        best_fit = [a0, b0, a, b, c, d, e,  delta]
                        min_delta = abs(delta)
    return best_fit


def write_results(a0, b0, a, b, c, d, e, delta):
    with open('gcf-search-progress.txt', 'a') as f:
        f.write(f"{a0},{b0},{a},{b},{c},{d},{e},{delta}\n")


if __name__ == '__main__':
    load_zeros()
    open('gcf-search-progress.txt', 'w').close()

    start_time = time.time()

    initial_terms_all = [1, 2, 3, 5, 7, 11, 13, 17, 19]

    start = 51
    end = 60

    for i in range(start, end+1):
        print(f"****Zero {i}****")
        pool = Pool(processes=3)
        set1 = pool.apply_async(gcf_search, (i, initial_terms_all[0:3], zeta_zeros_global))
        set2 = pool.apply_async(gcf_search, (i, initial_terms_all[3:6], zeta_zeros_global))
        set3 = pool.apply_async(gcf_search, (i, initial_terms_all[6:9], zeta_zeros_global))

        pool.close()
        pool.join()

        result1 = set1.get()
        result2 = set2.get()
        result3 = set3.get()

        deltas = [abs(result1[7]), abs(result2[7]), abs(result3[7])]
        index_min = min(range(len(deltas)), key=deltas.__getitem__)

        with open('gcf-search-progress.txt', 'a') as f:
            f.write(f"*****Zero #{i}*****\n")

        if index_min == 0:
            write_results(*result1[:7], f"{result1[7]:.8e}")
        elif index_min == 1:
            write_results(*result2[:7], f"{result2[7]:.8e}")
        else:
            write_results(*result3[:7], f"{result3[7]:.8e}")

        print(result1)
        print(result2)
        print(result3)

    print(f"Time elapsed: { time.time() - start_time } seconds")
