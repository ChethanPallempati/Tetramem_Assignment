from collections import deque
import numpy as np
import matplotlib.pyplot as plt
import cv2


def find_path(image, x1, y1, x2, y2):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #for grayscaling 
    rows, cols = image.shape[:2]

    # boundary check
    if not (0 <= x1 < cols and 0 <= y1 < rows):
        print("Out of bounds")
        return None

    if not (0 <= x2 < cols and 0 <= y2 < rows):
        print("Out of bounds")
        return None

    # must start/end on black space
    if image[y1, x1] != 0 or image[y2, x2] != 0:
        return None

    q = deque([(x1, y1)])
    visited = {(x1, y1)}
    parent = {}

    directions = [(1,0), (-1,0), (0,1), (0,-1)]

    while q:
        x, y = q.popleft()

        if (x, y) == (x2, y2):
            path = []
            cur = (x, y)

            while cur is not None:
                path.append(cur)
                cur = parent.get(cur)

            return path[::-1]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < cols and 0 <= ny < rows:
                if image[ny, nx] == 0 and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)
                    q.append((nx, ny))

    return None


def visualize_path(image, path):
    image = cv2.cvtColor(image, 0)

    plt.imshow(image, cmap="gray")
 #If no path is found
    if not path:
        plt.title("No Path Found")
        plt.show()
        return

    xs = [p[0] for p in path]
    ys = [p[1] for p in path]

    plt.plot(xs, ys, color="red", linewidth=2)
    plt.scatter(xs[0], ys[0], color="red", label="start_point")
    plt.scatter(xs[-1], ys[-1], color="green", label="end_point")

    plt.legend()
    plt.title("Path Visualization")
    plt.show()


# Test
if __name__ == "__main__":
    img = cv2.imread("bars.png", cv2.IMREAD_COLOR)
    path = find_path(img, 0, 0, 4, 1)
    visualize_path(img, path)