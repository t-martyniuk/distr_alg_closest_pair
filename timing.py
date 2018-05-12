import closest_pair
import threading
from time import time
import random
from matplotlib import pyplot as plt


degrees = list(range(3,8))
time_seq = []
time_par = []

for ii in degrees:
    length = pow(2,ii)
    p = []
    for i in range(length):
        p.append(closest_pair.Point(random.uniform(-1000, 1000), random.uniform(-1000, 1000)))
    p_x = sorted(p, key=closest_pair.getKeyX)
    p_y = sorted(p, key=closest_pair.getKeyY)

    t = time()
    seq_list = closest_pair.seq_closest_pair(p_x, p_y)
    t_new = time() - t
    time_seq.append(t_new)

    t = time()
    par_list = closest_pair.par_closest_pair(p_x, p_y)
    t_new = time() - t
    time_par.append(t_new)

plt.plot(degrees,time_seq)
plt.plot(degrees,time_par)
plt.legend(['seq','par'])
plt.show()