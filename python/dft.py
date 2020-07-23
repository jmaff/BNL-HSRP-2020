# Performs discrete fourier transform on a given input and plots the result
import math
import matplotlib.pyplot as plt


# A slightly modified implementation of DFT from the powerpoint - after viewing some other implementations online I
# made some changes to the original version to slim it down a bit, although I'm not sure if some of the changes would
# impact the performance of the transform (such as "ignoring" x data)
# some equations from https://www.youtube.com/watch?v=mkGsMWi_j4Q
# This returns a list of the same length as data consisting of 2-tuples with the cos and sin components from the dft
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

        f_cos = 2*f_cos/len(data)
        f_sin = 2 * f_sin / len(data)
        transform.append((f_cos, f_sin))
    return transform


# Returns a list of the amplitudes of the frequency bins (still need to understand why this appears so similar to the
# graph of the cos and sin data)
def dft_amp(transform):
    amp = []
    for term in transform:
        amp.append(math.sqrt(term[0]**2+term[1]**2))
    return amp


# data = [0, 0.707, 1, 0.707, 0, -0.707, -1, -0.707]  # 8 data points sampled from a sine wave

# generate data
num_samples = 100
dx = 2*math.pi/num_samples

data = []
x = 0
while num_samples > 0:
    data.append(29*math.cos(3*x)+7*math.cos(19*x)+17*math.sin(11*x)+2*math.sin(31*x))
    x += dx
    num_samples -= 1

transform = dft(data)
amps = dft_amp(transform)

# extract the terms from the result of dft
cos_terms = [term[0] for term in transform]
sin_terms = [term[1] for term in transform]

# TODO: adjust graph axes and labeling, add power graph
x_ord = [i for i in range(len(transform))]
plt.bar(x_ord, cos_terms, color='blue')
plt.bar(x_ord, sin_terms, color='red')

plt.show()
