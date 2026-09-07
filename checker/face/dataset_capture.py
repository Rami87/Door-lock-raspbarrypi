"""Capture face samples for one person, to be used by train.py.

Usage (run on the Pi, with a camera attached):
    python3 -m checker.face.dataset_capture <name> [num_samples]
"""
import os
import sys

import cv2

DATASET_DIR = os.path.join(os.path.dirname(__file__), "dataset")
# Bundled here rather than loaded from cv2.data.haarcascades: some
# opencv-contrib-python builds don't actually ship that data file.
CASCADE_PATH = os.path.join(os.path.dirname(__file__), "haarcascade_frontalface_default.xml")


def capture(name, num_samples=30, camera_index=0):
    face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
    cam = cv2.VideoCapture(camera_index)
    person_dir = os.path.join(DATASET_DIR, name)
    os.makedirs(person_dir, exist_ok=True)

    count = 0
    try:
        while count < num_samples:
            ret, frame = cam.read()
            if not ret:
                continue
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                count += 1
                face_img = gray[y:y + h, x:x + w]
                cv2.imwrite(os.path.join(person_dir, f"{count}.jpg"), face_img)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                if count >= num_samples:
                    break
            cv2.imshow("Capturing faces - press q to stop", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cam.release()
        cv2.destroyAllWindows()

    print(f"Captured {count} images for '{name}' in {person_dir}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 -m checker.face.dataset_capture <name> [num_samples]")
        sys.exit(1)
    person_name = sys.argv[1]
    samples = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    capture(person_name, samples)
