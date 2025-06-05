# backend/generate_stl.py
import numpy as np
import cv2
from PIL import Image
import io
from stl import mesh

def convert_sketch_to_stl(image_bytes):
    # Load and convert sketch image to grayscale
    image = Image.open(io.BytesIO(image_bytes)).convert("L")
    image_np = np.array(image)

    # Apply blur and edge detection
    blurred = cv2.GaussianBlur(image_np, (5, 5), 0)
    edges = cv2.Canny(blurred, 30, 100)

    # Use edges as a height map (0–5 range)
    height_map = (edges / 255.0) * 5
    rows, cols = height_map.shape

    vertices = []
    faces = []

    for i in range(rows - 1):
        for j in range(cols - 1):
            v0 = [i, j, height_map[i, j]]
            v1 = [i + 1, j, height_map[i + 1, j]]
            v2 = [i + 1, j + 1, height_map[i + 1, j + 1]]
            v3 = [i, j + 1, height_map[i, j + 1]]
            idx = len(vertices)
            vertices.extend([v0, v1, v2, v3])
            faces.extend([
                [idx, idx + 1, idx + 2],
                [idx, idx + 2, idx + 3]
            ])

    vertices_np = np.array(vertices)
    faces_np = np.array(faces)

    m = mesh.Mesh(np.zeros(faces_np.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces_np):
        for j in range(3):
            m.vectors[i][j] = vertices_np[f[j], :]

    buffer = io.BytesIO()
    m.save(buffer)
    return buffer.getvalue()