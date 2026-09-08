# model.py
import cv2
import numpy as np
import tensorflow as tf

import random


class MockClassifier:
    """Drop-in replacement for CornClassifier — returns random results, no model needed."""
    def __init__(self, model_path=None, healthy_bias=0.7):
        # healthy_bias: probability a given seed is classified "healthy" (0.0–1.0)
        self.healthy_bias = healthy_bias
        print("[MockClassifier] Initialized (no real model loaded)")

    def classify(self, image):
        is_healthy = random.random() < self.healthy_bias
        confidence = random.uniform(0.75, 0.99)
        pred_index = 0 if is_healthy else 1
        return pred_index, confidence

    def is_healthy(self, image, threshold=0.8):
        idx, conf = self.classify(image)
        return (idx == 0, conf)

class CornClassifier:
    """Loads and runs the TFLite model."""
    def __init__(self, model_path):
        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.input_height = self.input_details[0]['shape'][1]
        self.input_width = self.input_details[0]['shape'][2]
        self.healthy_index = 0
        self.unhealthy_index = 1

    def classify(self, image):
        img = cv2.resize(image, (self.input_width, self.input_height))
        input_data = np.expand_dims(img, axis=0).astype(np.float32)
        # input_data = input_data / 255.0  # uncomment if model expects 0-1 range

        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()
        output = self.interpreter.get_tensor(self.output_details[0]['index'])
        pred_index = np.argmax(output[0])
        confidence = output[0][pred_index]
        return pred_index, confidence

    def is_healthy(self, image, threshold=0.8):
        idx, conf = self.classify(image)
        return (idx == self.healthy_index, conf)