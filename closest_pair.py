import threading
import random
import math

class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y


    def __repr__(self):
        return '({}, {})'.format(self._x, self._y)

def distance(p1, p2):
    return math.sqrt((p1._x - p2._x)**2 + (p1._y - p2._y)**2)

def brute_force_closest_pair(p):
    if len(p) < 2:
        return p, float('inf')
    else:
        d = float('inf')
        idx1 = 0
        idx2 = 1
        for i in range(len(p)):
            for j in range(i + 1, len(p)):
                if distance(p[i], p[j]) < d:
                    d = distance(p[i], p[j])
                    idx1, idx2 = i, j
        point1 = p[idx1]
        point2 = p[idx2]

        return (point1, point2), d


def getKeyX(point):
    return point._x

def getKeyY(point):
    return point._y

def boundary_merge(py, delta, x_m):
    s_y = list(filter(lambda el: abs(el._x - x_m._x) <= delta, py))
    best = delta
    best_pair = (py[0], py[1])
    for i in range(len(s_y)):
        for j in range(1, min(8, len(s_y) - i)):
            p1 = s_y[i]
            p2 = s_y[i+j]
            if distance(p1, p2) < best:
                best = distance(p1, p2)
                best_pair = (p1, p2)

    return best_pair, best


def seq_closest_pair(px, py):
    if (len(px) <= 3):
        return brute_force_closest_pair(px)
    length_p = len(px)
    lx = px[:(length_p//2)]
    rx = px[(length_p//2):]
    ly, ry = [], []
    for el in py:
        if el in lx:
            ly.append(el)
        else:
            ry.append(el)
    pair1, dist1 = seq_closest_pair(lx, ly)
    pair2, dist2 = seq_closest_pair(rx, ry)
    delta = min(dist1, dist2)
    pair3, dist3 = boundary_merge(py, delta, lx[-1])
    if dist3 < delta:
        return pair3, dist3
    elif dist2 < dist1:
        return pair2, dist2
    else:
        return pair1, dist1


def closest_pair_help(lx,ly,res_list):
    res_list.append(par_closest_pair(lx,ly))


def par_closest_pair(px, py):
    if (len(px) <= 3):
        return brute_force_closest_pair(px)
    length_p = len(px)
    lx = px[:(length_p//2)]
    rx = px[(length_p//2):]
    ly, ry = [], []
    for el in py:
        if el in lx:
            ly.append(el)
        else:
            ry.append(el)
    res_list = []
    p1 = threading.Thread(target=closest_pair_help, args=(lx, ly, res_list))

    p1.start()
    p2 = threading.Thread(target=closest_pair_help, args=(rx, ry, res_list))

    p2.start()
    p1.join()
    p2.join()


    pair1, dist1 = res_list[0]
    pair2, dist2 = res_list[1]
    delta = min(dist1, dist2)
    pair3, dist3 = boundary_merge(py, delta, lx[-1])
    if dist3 < delta:
        return pair3, dist3
    elif dist2 < dist1:
        return pair2, dist2
    else:
        return pair1, dist1


p = []
for i in range(4000):
    p.append(Point(random.uniform(-1000,1000), random.uniform(-1000,1000)))

p_x = sorted(p, key=getKeyX)
p_y = sorted(p, key=getKeyY)

print('Sequential closest pair', seq_closest_pair(p_x, p_y))

print('Parallel closest pair', par_closest_pair(p_x, p_y))

print('Brute-force closest pair', brute_force_closest_pair(p))


