import cv2
import numpy as np
import os
from population import Population
from config import GENERATIONS

if __name__ == '__main__':
    target_image = cv2.imread('lenna.png', cv2.IMREAD_UNCHANGED)

    if target_image.shape[2] == 3:
        target_image = np.concatenate([target_image, 255 * np.ones((*target_image.shape[:2], 1), dtype=np.uint8)], axis=2)

    generations = GENERATIONS
    population = Population(target_image=target_image)
    population.evaluate()
    gen = 0

    while True:
        population.next_generation()
        best, best_fitness = population.getBest()
        img = best.draw()

        if gen % 10 == 0:
            img_show = img.copy()
            target_show = target_image.copy()
            
            if img_show.shape[2] == 4:
                img_show = cv2.cvtColor(img_show, cv2.COLOR_BGRA2BGR)
            
            if target_show.shape[2] == 4:
                target_show = cv2.cvtColor(target_show, cv2.COLOR_BGRA2BGR)
            both = np.hstack([target_show, img_show])
            window_title = 'Target (left) vs Best Chromosome (right)'
            cv2.imshow(window_title, both)
            cv2.setWindowTitle(window_title, f'{window_title} | Best fitness: {best_fitness:.6f}')
            
            if gen % 50 == 0:
                os.makedirs('results', exist_ok=True)
                filename = f'results/gen_{gen+1}_fitness_{best_fitness:.4f}.png'
                cv2.imwrite(filename, img_show)
            
            if cv2.waitKey(1) & 0xFF == 27:
                break
            print(f'Generation: {gen+1}, fitness: {best_fitness:.10f}')

        gen += 1

    cv2.destroyAllWindows()
