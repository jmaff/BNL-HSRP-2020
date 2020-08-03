# Performs discrete fourier transform on a given input and plots the result
import math
import matplotlib.pyplot as plt


# A slightly modified implementation of DFT from the powerpoint - doesn't take in x-data and instead uses
# converts ordinal numbers to 0 to 2*pi since all the data I'm dealing with is ordinal
# This returns a list of the same length as data consisting of 2-tuples with the cos and sin terms from the dft
def dft(data):
    transform = []
    # only can create frequency bins up to this limit
    nyquist_limit = int(len(data) / 2)

    for k in range(0, nyquist_limit):
        f_cos = 0
        f_sin = 0

        for n in range(len(data)):
            f_cos += data[n]*math.cos((2*math.pi*k*n)/len(data))
            f_sin += data[n]*math.sin((2*math.pi*k*n)/len(data))

        if k > 0:
            f_cos = 2*f_cos/len(data)
            f_sin = 2 * f_sin / len(data)
        else:
            f_cos = f_cos / len(data)
            f_sin = f_sin / len(data)

        transform.append((f_cos, f_sin))

    return transform


# Returns power data
def dft_power(transform):
    power = []
    for term in transform:
        power.append(math.sqrt(term[0]**2+term[1]**2))
    return power


def plot_dft(transform, pos, title):
    # extract the terms from the result of dft
    plt.subplot(*pos)
    plt.title(title)
    cos_terms = [term[0] for term in transform]
    sin_terms = [term[1] for term in transform]

    x_ord = [i for i in range(len(transform))]
    plt.bar(x_ord, cos_terms, color='blue', label='cos')
    plt.bar(x_ord, sin_terms, color='red', label='sin')
    plt.legend(loc='upper right')


def idft(transform, sample_count):
    y_est = []
    for i in range(sample_count):
        x = (2 * math.pi * i) / sample_count
        y = 0
        for n in range(len(transform)):
            y += transform[n][0] * math.cos(n * x)
            y += transform[n][1] * math.sin(n * x)
        y_est.append(y)

    return y_est


# num_samples = 100
# dx = 2*math.pi/num_samples
#
# data = []
# x = 0
# while num_samples > 0:
#     # data.append(29*math.cos(3*x)+7*math.cos(19*x)+17*math.sin(11*x)+2*math.sin(31*x))
#     data.append(math.sin(x))
#     x += dx
#     num_samples -= 1
#
# transform = dft(data)
# reconstructed = idft(transform, len(data))
#
#
# plt.plot(reconstructed)
# plt.show()
