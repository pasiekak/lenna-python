import numpy as np

from config import IMAGE_HEIGHT, IMAGE_WIDTH, NUMBER_OF_TRIANGLES
from triangle import Triangle

class Chromosome:
    def __init__(self):
        self._cached_img = None
        self.fitness_score = None

        random_color = [np.random.randint(0, 256) for _ in range(4)]
        self.background = np.full((IMAGE_HEIGHT, IMAGE_WIDTH, 4), random_color, dtype=np.uint8)
        self.triangles = [Triangle.random() for _ in range(NUMBER_OF_TRIANGLES)]
        self._last_hash = None

    def draw(self):
        triangles_hash = hash(tuple(tuple(t.coords) + tuple(t.color) for t in self.triangles))
        
        if self._cached_img is not None and self._last_hash == triangles_hash:
            return self._cached_img
        
        img = self.background.copy()
        
        for triangle in self.triangles:
            triangle.draw(img)
        
        self._cached_img = img
        self._last_hash = triangles_hash
        return img

    def getImage(self):
        return self.draw()

    # MSE fitness function
    def fitness(self, target_img, use_deltaE=False):
        img = self.draw()[..., :3].astype(np.float32)
        target = target_img[..., :3].astype(np.float32)
        mse = np.mean((img - target) ** 2)
        self.fitness_score = 1 / (1 + mse)
        return self.fitness_score