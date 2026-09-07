"""Train the LBPH face recognizer from images captured by dataset_capture.py.

Usage:
    python3 -m checker.face.train
"""
import json
import os

import cv2
import numpy as np

DATASET_DIR = os.path.join(os.path.dirname(__file__), "dataset")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "trainer.yml")
LABELS_PATH = os.path.join(os.path.dirname(__file__), "labels.json")


def train():
    if not os.path.isdir(DATASET_DIR):
        raise RuntimeError(
            f"No dataset found at {DATASET_DIR}. Run dataset_capture.py for each "
            "authorized person first."
        )

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces = []
    labels = []
    label_map = {}

    for idx, name in enumerate(sorted(os.listdir(DATASET_DIR))):
        person_dir = os.path.join(DATASET_DIR, name)
        if not os.path.isdir(person_dir):
            continue
        label_map[idx] = name
        for filename in os.listdir(person_dir):
            img = cv2.imread(os.path.join(person_dir, filename), cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            faces.append(img)
            labels.append(idx)

    if not faces:
        raise RuntimeError(f"No training images found under {DATASET_DIR}")

    recognizer.train(faces, np.array(labels))
    recognizer.save(MODEL_PATH)
    with open(LABELS_PATH, "w") as f:
        json.dump(label_map, f)

    print(f"Trained on {len(faces)} images across {len(label_map)} people -> {MODEL_PATH}")


if __name__ == "__main__":
    train()
