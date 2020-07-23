# decodes a generalized continued fraction given the formulas for a_n and b_n mainly off of the form of
# a_n = a_i*n^2+b_i*n+c, b_n = d_i*n+e_i (I don't yet know how to get these coefficients)
import math


a0 = 8
b0 = 2
actual = math.pi

# Coefficients for a_n and b_n [a_i, b_i, c_i, d_i, e_i]
coeff = [4, 8, 0, 4, 2]  # PI, from the first version of the Project Overview powerpoint


def a(n):
    return a0 if n == 0 else coeff[0]*(n**2)+coeff[1]*n+coeff[2]  # given in Research Project Overview pptx
    # return a0 if n == 0 else 6


def b(n):
    return b0 if n == 0 else coeff[3]*n+coeff[4]  # given in Research Project Overview pptx
    # return b0 if n == 0 else (2*n+1)**2


# this is the modified h/k algorithm for GCFs - for some reason, this doesn't work with the GCFs of the form given for
# the zeta zeros or the alternate GCF for pi (with a_n = a_i*n^2+b_i*n...), but does for the pi GCF from Session 12
def decode_other_form(iterations):
    print(f"{'a':>5}{'b':>5}{'h':>15}{'k':>15}{'convergent':>20}")
    h = [0, 1]
    k = [1, 0]

    for n in range(2, iterations+1+2):
        h.append(a(n-2)*h[n-1]+b(n-1-2)*h[n-2])
        k.append(a(n-2)*k[n-1]+b(n-1-2)*k[n-2])

        convergent = h[n]/k[n]
        print(f"{a(n-2):>5.0f}{b(n-2):>5.0f}{h[n]:>15.5E}{k[n]:>15.5E}{convergent:>20.14f}")


# This is a simple recursive method I wrote for finding the decimal approximation of the given GCF to a desired number
# of iterations
def decode_recursive(max_n, n):
    if n == max_n:
        return a(n) / b(n)
    else:
        return b(n) + (a(n) / decode_recursive(max_n, n+1))


print(f"{decode_recursive(24, 0):.20f}")  # prints 3.14159265358979311600
