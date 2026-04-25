from collections import deque
import numpy as np
import cv2
#Function to check if there is a path between two co-ordinates
def path_exists(image, x1, y1, x2, y2):
    #dimensions
    rows, cols = image.shape
    
    # boundary check
    if not (0 <= x1 < cols and 0 <= y1< rows):
        print("Out of bounds")
        return False
    if not (0 <= x2 < cols and 0 <= y2 < rows): 
        print("Out of bounds")
        return False

    # To check if start/end is black
    if image[y1][x1] != 0 or image[y2][x2] != 0:
        return False
   #BFS(to find shortest path) 
    q = deque([(x1, y1)])
    visited = set([(x1, y1)])

    directions = [(1,0), (-1,0), (0,1), (0,-1)]

    while q:
        x, y = q.popleft()
        if (x, y) == (x2,y2):
            return True
        for ux, uy in directions:
            nx, ny = x + ux, y + uy
            if 0 <= nx < cols and 0 <= ny < rows:
                if (nx, ny) not in visited and image[ny][nx] == 0:
                    visited.add((nx, ny))
                    q.append((nx, ny))

    return False
#Test
if __name__ == "__main__":
    #Load image in grayscale to avoid overwhelming
    img = cv2.imread("polygons.png", cv2.IMREAD_COLOR)
    result = path_exists(img, 10, 10, 10, 13)
    print("Path exists:", result)