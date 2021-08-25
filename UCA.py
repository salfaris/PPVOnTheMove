import numpy as np

def uca(A, B, ra, rb):
    len_AB = np.sqrt((A[0] - B[0])**2 + (A[1] - B[1])**2)
    t = (ra - rb + len_AB)/(2*len_AB)
    mid = A + t * B
    
    return mid

# Test Case
A = np.array([0, 0])
B = np.array([4, -4])
ra = 3
rb = 5

print(uca(A, B, ra, rb))
