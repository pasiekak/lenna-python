import cv2
import numpy as np
from config import IMAGE_WIDTH, IMAGE_HEIGHT, TRIANGLE_MAX_EDGE_LENGTH, TRIANGLE_MAX_ANGLE, TRIANGLE_MIN_ANGLE

class Triangle:
    def __init__(self, coords, color):
        self.coords = coords
        self.color = color

    @classmethod
    def random(cls):
        def clamp(val, minval, maxval):
            return max(minval, min(val, maxval))
        def offset_point(x, y):
            angle = np.random.uniform(0, 2 * np.pi)
            length = np.random.uniform(0, TRIANGLE_MAX_EDGE_LENGTH)
            dx = np.cos(angle) * length
            dy = np.sin(angle) * length
            return clamp(int(x + dx), 0, IMAGE_WIDTH), clamp(int(y + dy), 0, IMAGE_HEIGHT)
        def angle_between(p1, p2, p3):
            a = np.linalg.norm(np.array(p2) - np.array(p1))
            b = np.linalg.norm(np.array(p2) - np.array(p3))
            c = np.linalg.norm(np.array(p1) - np.array(p3))
            denom = 2 * a * b
            if denom == 0:
                return 0
            arg = (a ** 2 + b ** 2 - c ** 2) / denom
            arg = np.clip(arg, -1.0, 1.0)
            try:
                angle_rad = np.arccos(arg)
                return np.degrees(angle_rad)
            except:
                return 0
        for _ in range(100):
            x1, y1 = np.random.randint(0, IMAGE_WIDTH), np.random.randint(0, IMAGE_HEIGHT)
            x2, y2 = offset_point(x1, y1)
            x3, y3 = offset_point(x1, y1)
            coords = [(x1, y1), (x2, y2), (x3, y3)]
            angles = [
                angle_between(coords[1], coords[0], coords[2]),
                angle_between(coords[0], coords[1], coords[2]),
                angle_between(coords[0], coords[2], coords[1]),
            ]
            if all(TRIANGLE_MIN_ANGLE <= a <= TRIANGLE_MAX_ANGLE for a in angles):
                color = (
                    np.random.randint(0, 256),
                    np.random.randint(0, 256),
                    np.random.randint(0, 256),
                    np.random.randint(0, 256)
                )
                return cls(coords, color)
        return cls([(x1, y1), (x2, y2), (x3, y3)], (0, 0, 0, 0))

    def draw(self, img):
        pts = np.array(self.coords, np.int32).reshape((-1, 1, 2))
        color = tuple(int(c) for c in self.color)
        cv2.fillPoly(img, [pts], color)

    def mutate(self, delta=5):
        coords_arr = np.array(self.coords, dtype=np.int32)
        noise = np.random.randint(-delta, delta+1, coords_arr.shape)
        coords_arr = coords_arr + noise
        coords_arr[:,0] = np.clip(coords_arr[:,0], 0, IMAGE_WIDTH)
        coords_arr[:,1] = np.clip(coords_arr[:,1], 0, IMAGE_HEIGHT)
        self.coords = [tuple(x) for x in coords_arr.tolist()]
        r, g, b, a = self.color
        if np.random.rand() < 0.5:
            r = min(255, max(0, r + np.random.randint(-delta * 10, delta * 10)))
        if np.random.rand() < 0.5:
            g = min(255, max(0, g + np.random.randint(-delta * 10, delta * 10)))
        if np.random.rand() < 0.5:
            b = min(255, max(0, b + np.random.randint(-delta * 10, delta * 10)))
        if np.random.rand() < 0.5:
            a = min(255, max(0, a + np.random.randint(-delta * 5, delta * 5)))
        self.color = (r, g, b, a)