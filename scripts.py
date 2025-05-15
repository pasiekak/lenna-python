import cv2
import glob
import re
import os
import numpy as np

def make_video_from_results(folder='results', output='output.mp4', fps=10, codec='mp4v'):
    img_files = glob.glob(os.path.join(folder, 'gen_*_fitness_*.png'))

    def extract_gen(filename):
        match = re.search(r'gen_(\d+)_fitness_', filename)
        return int(match.group(1)) if match else -1

    img_files_sorted = sorted(img_files, key=extract_gen)

    if not img_files_sorted:
        print("Brak plików do połączenia.")
        return

    frame = cv2.imread(img_files_sorted[0])
    height, width, layers = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*codec)
    out = cv2.VideoWriter(output, fourcc, fps, (width, height))

    for filename in img_files_sorted:
        img = cv2.imread(filename)
        if img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        out.write(img)

    out.release()
    print(f"Film zapisany jako {output} (codec: {codec}, fps: {fps})")

if __name__ == "__main__":
    # MP4 z kodekiem mp4v (zalecane dla Windows/OpenCV)
    make_video_from_results('results', 'output.mp4', fps=8, codec='mp4v')