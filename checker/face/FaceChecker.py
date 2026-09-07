import json
import os
import time

import cv2

MODEL_PATH = os.path.join(os.path.dirname(__file__), "trainer.yml")
LABELS_PATH = os.path.join(os.path.dirname(__file__), "labels.json")
# Bundled here rather than loaded from cv2.data.haarcascades: some
# opencv-contrib-python builds don't actually ship that data file.
CASCADE_PATH = os.path.join(os.path.dirname(__file__), "haarcascade_frontalface_default.xml")

# LBPH confidence is a distance: lower means a closer match. Anything below
# this is treated as a recognized, authorized face.
CONFIDENCE_THRESHOLD = 70
DEFAULT_TIMEOUT_SECONDS = 10


class Face_checker:
    def __init__(self, camera_index=0):
        if not os.path.exists(MODEL_PATH) or not os.path.exists(LABELS_PATH):
            raise RuntimeError(
                "No trained face model found. Run "
                "'python3 -m checker.face.dataset_capture <name>' then "
                "'python3 -m checker.face.train' first."
            )
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read(MODEL_PATH)
        with open(LABELS_PATH) as f:
            self.labels = {int(k): v for k, v in json.load(f).items()}
        self.face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
        self.camera_index = camera_index

    def auth(self):
        identity = self.recognize()
        return identity is not None and identity != "unknown"

    def recognize(self, timeout=DEFAULT_TIMEOUT_SECONDS):
        """Look for a face for up to `timeout` seconds.

        Returns the matched person's name, "unknown" if a face was seen but
        didn't match anyone closely enough, or None if no face was seen at all.
        """
        cam = cv2.VideoCapture(self.camera_index)
        start = time.time()
        try:
            while time.time() - start < timeout:
                ret, frame = cam.read()
                if not ret:
                    continue
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    label, confidence = self.recognizer.predict(gray[y:y + h, x:x + w])
                    if confidence < CONFIDENCE_THRESHOLD:
                        return self.labels.get(label, "unknown")
                    return "unknown"
            return None
        finally:
            cam.release()
