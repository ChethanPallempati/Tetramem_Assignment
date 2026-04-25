import cv2
import copy
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


# make graph from the image
def mk(img):
    r, c = img.shape
    g = nx.DiGraph()
    d = [(1,0), (-1,0), (0,1), (0,-1)]

    def ii(x, y):
        return "in_" + str(x) + "_" + str(y)
    def oo(x, y):
        return "out_" + str(x) + "_" + str(y)
    for y in range(r):
        for x in range(c):
            # skip if blocked
            if img[y][x] != 0:
                continue
            # split node so path cant reuse same cell
            g.add_edge(ii(x, y), oo(x, y), capacity=1)
            for dx, dy in d:
                nx1 = x + dx
                ny1 = y + dy
                # check bounds first
                if 0 <= nx1 < c and 0 <= ny1 < r:
                    if img[ny1][nx1] == 0:
                        g.add_edge(oo(x, y), ii(nx1, ny1), capacity=1)
    return g

# get one path from the flow
def gp(f, s, t):
    p = [s]
    cur = s
    while cur != t:
        nxt = None

        for k, v in f[cur].items():
            if v > 0:
                nxt = k
                f[cur][k] -= 1   # use it once
                break
        if nxt is None:
            return None
        p.append(nxt)
        cur = nxt
    return p


# main part
def run(img, s1, e1, s2, e2):

    # if color image, just use one channel
    if len(img.shape) == 3:
        img = img[:, :, 0]

    g = mk(img)
    s = "S"
    t = "T"
    def ii(x, y):
        return "in_" + str(x) + "_" + str(y)

    def oo(x, y):
        return "out_" + str(x) + "_" + str(y)

    # connect starts
    g.add_edge(s, ii(*s1), capacity=1)
    g.add_edge(s, ii(*s2), capacity=1)

    # connect ends
    g.add_edge(oo(*e1), t, capacity=1)
    g.add_edge(oo(*e2), t, capacity=1)

    fv, fd = nx.maximum_flow(g, s, t)

    # means two full paths dont exist
    if fv < 2:
        return False, None, None

    fc = copy.deepcopy(fd)

    p1 = gp(fc, s, t)
    p2 = gp(fc, s, t)

    return True, p1, p2


# show both paths
def sh(img, p1, p2):

    if len(img.shape) == 2:
        res = np.stack([img, img, img], axis=-1)
    else:
        res = img.copy()

    def dr(p, col):
        if p is None:
            return

        for n in p:
            if n == "S" or n == "T":
                continue

            if n.startswith("in_"):
                x, y = map(int, n.replace("in_", "").split("_"))
                res[y, x] = col

    # red path
    dr(p1, [255, 0, 0])

    # blue path
    dr(p2, [0, 0, 255])

    plt.figure(figsize=(6, 6))
    plt.imshow(res)
    plt.axis("off")
    plt.show()


img = cv2.imread("/Users/chetanpallempati/Downloads/bars.png")

s1, e1 = (0, 0), (0, 10)
s2, e2 = (2, 0), (2, 9)

ok, p1, p2 = run(img, s1, e1, s2, e2)

print("Paths exist:", ok)

sh(img, p1, p2)
