import cf
import decimal

zeta_zeros = []


def load_zeros():
    with open('ZetaZeroes1024.txt', 'r') as f:
        for line in f:
            if line == '\n' or line == '  \n':
                zeta_zeros.append('')
            else:
                zeta_zeros[len(zeta_zeros) - 1] += line.strip()
    zeta_zeros.pop()


decimal.getcontext().prec = 1025
dec = decimal.Decimal

load_zeros()
zero0 = cf.hk_quadlin_gen_decode(13, 13, (-13, 13, -13, 13, -1), 15, actual=dec(zeta_zeros[0]))
delta0 = dec(zeta_zeros[0]) - cf.hk_decode_to_decimal(zero0)
print(f"{delta0:.20e}")

zero1 = cf.hk_quadlin_gen_decode(17, 11, (-5, 3, -7, 5, -1), 15, actual=dec(zeta_zeros[1]))
delta1 = dec(zeta_zeros[1]) - cf.hk_decode_to_decimal(zero1)
print(f"{delta1:.20e}")
