# This is the C++ code from Session 21 pretty much directly translated into python (requires x data)
import math


def dft(data):
    # scale x data to radians
    nyquist_limit = int(len(data)/2)
    for i in range (len(data)):
        scaled_x = data[i][0]*(2*math.pi/len(data))
        data[i] = (scaled_x, data[i][1])

    transform = []

    for k in range(nyquist_limit):
        f_cos = 0
        f_sin = 0

        for n in range(len(data)):
            x = data[n][0]
            y = data[n][1]
            f_cos += y*math.cos(k*x)
            f_sin += y*math.sin(k*x)

        f_cos /= len(data)
        f_sin /= len(data)

        if k > 0:
            f_cos *= 2
            f_sin *= 2

        transform.append((f_cos, f_sin))

    return transform


def dft_amp(transform):
    f_y = []
    for term in transform:
        f_y.append(math.sqrt(term[0]**2+term[1]**2))
    return f_y


data = [(0, 0), (1, 0.707), (2, 1), (3, 0.707), (4, 0), (5, -0.707), (6, -1), (7, -0.707)]
print(dft_amp(dft(data)))
