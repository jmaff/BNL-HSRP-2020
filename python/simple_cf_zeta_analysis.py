import cf
import decimal
import matplotlib.pyplot as plt
import dft


zeta_zeros = []  # high-precision zeros of the zeta function (from file)
lrss = []  # longest-repeated subsequence in the cf encoding of each zero
lrss_lengths = []  # lengths of the LRSS above
lrss_first_index = []
max_values = []  # maximum term (a) in the cf encoding of each zero
zero_1_simple_cf = []
zero_1_successive_diffs = []

lrss_lengths_dft = []
lrss_first_index_dft = []
max_value_dft = []
zero_1_simple_cf_dft = []
zero_1_successive_diffs_dft = []


def load_zeros():
    with open('ZetaZeroes1024.txt', 'r') as f:
        for line in f:
            if line == '\n' or line == '  \n':
                zeta_zeros.append('')
            else:
                zeta_zeros[len(zeta_zeros) - 1] += line.strip()
    zeta_zeros.pop()


def find_sub(sublist, list):
    for index in (i for i, e in enumerate(list) if e==sublist[0]):
        if list[index:index+len(sublist)] == sublist:
            return index


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
        lrss_first_index.append(find_sub(lrss_cf, zero_cf))
        max_values.append(max(zero_cf))

    global zero_1_simple_cf
    zero_1_simple_cf = simple_encode_zeta_zero(0)
    global zero_1_successive_diffs
    zero_1_successive_diffs = [zero_1_simple_cf[i+1] - zero_1_simple_cf[i] for i in range(len(zero_1_simple_cf)-1)]

    print(lrss)
    print(lrss_lengths)
    print(lrss_first_index)
    print(max_values)
    print(zero_1_successive_diffs)


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


def simple_cf_dft_analysis():
    global lrss_lengths_dft
    lrss_lengths_dft = dft.dft(lrss_lengths)
    global lrss_first_index_dft
    lrss_first_index_dft = dft.dft(lrss_first_index)
    global max_value_dft
    max_value_dft = dft.dft(max_values)
    global zero_1_simple_cf_dft
    zero_1_simple_cf_dft = dft.dft(zero_1_simple_cf)
    global zero_1_successive_diffs_dft
    zero_1_successive_diffs_dft = dft.dft(zero_1_successive_diffs)


def plot_cf_dft():
    plt.figure(1)
    plt.suptitle("Zeta Zeros Simple CF DFT (1/2)")
    dft.plot_dft(lrss_lengths_dft, (2, 3, 1), "LRSS Lengths DFT")
    dft.plot_dft(max_value_dft, (2, 3, 2), "Max Value DFT")
    dft.plot_dft(zero_1_simple_cf_dft, (2, 3, 3), "Simple CF Terms of Zeta Zero 1 DFT")

    plt.subplot(2, 3, 4)
    plt.plot(lrss_lengths, '-b', label="Original")
    plt.plot(dft.idft(lrss_lengths_dft, len(lrss_lengths)), ':r', label="IDFT")
    plt.legend(loc='upper right')

    plt.subplot(2, 3, 5)
    plt.plot(max_values, '-b', label="Original")
    plt.plot(dft.idft(max_value_dft, len(max_values)), ':r', label="IDFT")
    plt.legend(loc='upper right')

    plt.subplot(2, 3, 6)
    plt.plot(zero_1_simple_cf, '-b', label="Original")
    plt.plot(dft.idft(zero_1_simple_cf_dft, 1024), ':r', label="IDFT")
    plt.legend(loc='upper right')

    # FIGURE 2
    plt.figure(2)
    plt.suptitle("Zeta Zeros Simple CF DFT (2/2)")
    dft.plot_dft(lrss_first_index_dft, (2, 2, 1), "LRSS First Index DFT")
    dft.plot_dft(zero_1_successive_diffs_dft, (2, 2, 2), "Zero 1 Successive Diffs DFT")
    plt.legend(loc='upper right')

    plt.subplot(2, 2, 3)
    plt.plot(lrss_first_index, '-b', label="Original")
    plt.plot(dft.idft(lrss_first_index_dft, len(max_values)), ':r', label="IDFT")
    plt.legend(loc='upper right')

    plt.subplot(2, 2, 4)
    plt.plot(zero_1_successive_diffs, '-b', label="Original")
    plt.plot(dft.idft(zero_1_successive_diffs_dft, 1024), ':r', label="IDFT")
    plt.legend(loc='upper right')


load_zeros()
analyze_simple_zeta_cf()
simple_cf_dft_analysis()
plot_cf_dft()

plt.tight_layout()
plt.show()
