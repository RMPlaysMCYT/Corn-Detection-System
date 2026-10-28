# model.py
import cv2
import numpy as np
import tensorflow as tf
import random

class MockClassifier:
    def __init__(self, model_path=None, healthy_bias=0.7):
        self.healthy_bias = healthy_bias
        print("[MockClassifier] Initialized (no real model loaded)")

    def classify(self, image):
        is_healthy = random.random() < self.healthy_bias
        confidence = random.uniform(0.75, 0.99)
        pred_index = 0 if is_healthy else 1
        return pred_index, confidence

    def is_healthy(self, image, threshold=0.8):
        idx, conf = self.classify(image)
        return (idx == 0 and conf >= threshold, conf)

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
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (self.input_width, self.input_height))
        input_data = np.expand_dims(img, axis=0).astype(np.float32) / 255.0
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()
        output = self.interpreter.get_tensor(self.output_details[0]['index'])
        probabilities = output[0]
        if probabilities.size == 1:
            unhealthy_probability = float(probabilities[0])
            pred_index = int(unhealthy_probability >= 0.5)
            confidence = (unhealthy_probability if pred_index == 1
                          else 1.0 - unhealthy_probability)
        else:
            pred_index = int(np.argmax(probabilities))
            confidence = float(probabilities[pred_index])
        return pred_index, confidence

    def is_healthy(self, image, threshold=0.8):
        idx, conf = self.classify(image)
        return (idx == self.healthy_index and conf >= threshold, conf)
