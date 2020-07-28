import cf
import decimal
import matplotlib.pyplot as plt


zeta_zeros = []  # high-precision zeros of the zeta function (from file)
lrss = []  # longest-repeated subsequence in the cf encoding of each zero
lrss_lengths = []  # lengths of the LRSS above
max_values = []  # maximum term (a) in the cf encoding of each zero


def load_zeros():
    with open('ZetaZeroes1024.txt', 'r') as f:
        for line in f:
            if line == '\n' or line == '  \n':
                zeta_zeros.append('')
            else:
                zeta_zeros[len(zeta_zeros) - 1] += line.strip()
    zeta_zeros.pop()


# n is the nth zero (zero indexed)
def simple_encode_zeta_zero(n, disp=False):
    # Set up decimal context for high precision
    decimal.getcontext().prec = 1025
    dec = decimal.Decimal

    original = dec(zeta_zeros[n])
    encoded = cf.simple_encode(original, 1024)

    # print the original zero, the simple cf encoding, the decoding (fraction form), and decimal decoding
    if disp:
        decoded = cf.hk_simple_decode(encoded)
        decoded_dec = dec(decoded[0]) / dec(decoded[1])
        print(original)
        print(encoded)
        print(decoded)
        print(decoded_dec)

    return encoded


# encodes all 100 high precision zeros and populates the relevant lists
def analyze_simple_zeta_cf():
    for i in range(100):
        zero_cf = simple_encode_zeta_zero(i)
        lrss_cf = cf.lrss(zero_cf)
        lrss.append(lrss_cf)
        lrss_lengths.append(len(lrss_cf))
        max_values.append(max(zero_cf))


    print(lrss)
    print(lrss_lengths)
    print(max_values)


# plots the LRSS and greatest term data
def plot_simple_zeta_analysis():
    x_ord = [x for x in range(100)]
    plt.suptitle("Zeta Zeros Simple CF Analysis")
    plt.subplot(2, 2, 1)
    plt.scatter(x_ord, lrss_lengths, marker='s', s=2)
    plt.xlabel('Zeta Zero Ordinal Number')
    plt.ylabel('Longest-Recurring Subsequence Length')
    plt.title('LRSS Length')

    plt.subplot(2, 2, 2)
    plt.plot(x_ord, lrss_lengths, '-sb', markersize=2)
    plt.xlabel('Zeta Zero Ordinal Number')
    plt.ylabel('Longest-Recurring Subsequence Length')
    plt.title('LRSS Length (connected)')

    plt.subplot(2, 2, 3)
    plt.scatter(x_ord, max_values, marker='s', s=2)
    plt.xlabel('Zeta Zero Ordinal Number')
    plt.ylabel('Greatest Simple CF Term')
    plt.title('Greatest Simple CF Term')

    plt.subplot(2, 2, 4)
    plt.plot(x_ord, max_values, '-sg', markersize=2)
    plt.xlabel('Zeta Zero Ordinal Number')
    plt.ylabel('Greatest Simple CF Term')
    plt.title('Greatest Simple CF Term (connected)')

    plt.tight_layout()
    plt.show()


load_zeros()  # read the zeros from file and store in zeta_zeros
# analyze_simple_zeta_cf()  # find lrss and max terms
# plot_simple_zeta_analysis()  # plot this data

simple_encode_zeta_zero(0, disp=True)  # test first zero encode and decode
print()

# testing h/k decoding of the "pi" form generalized cf for zeta zero #2 (from powerpoint)
quadlin_test = cf.hk_quadlin_gen_decode(17, 11, (-5, 3, -7, 5, -1), 15)
print(cf.hk_decode_to_decimal(quadlin_test))
