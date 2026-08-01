import time
import numpy as np
import cv2
from tflite_runtime.interpreter import Interpreter
from gpiozero import AngularServo

# --- 1. Setup Servo ---
# Using GPIO 18. The min/max pulse widths might need slight tweaking 
# depending on your specific SG90 for accurate 0-180 degree movement.
servo = AngularServo(18, min_pulse_width=0.0006, max_pulse_width=0.0023)
DEFAULT_ANGLE = 0
REJECT_ANGLE = 90

def reject_seed():
    """Rotates servo to reject bin, then returns to default."""
    print("Rejecting seed!")
    servo.angle = REJECT_ANGLE
    time.sleep(0.5) # Give the seed time to fall
    servo.angle = DEFAULT_ANGLE
    time.sleep(0.5) # Wait for servo to return

# Ensure servo starts in default position
servo.angle = DEFAULT_ANGLE

# --- 2. Setup TFLite Model ---
MODEL_PATH = "path/to/your/seed_model.tflite"
interpreter = Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

# --- 3. Setup Camera (using OpenCV) ---
cap = cv2.VideoCapture(0) # 0 is usually the default USB/Pi camera

def classify_image(image):
    """Runs inference on the image and returns the predicted index and confidence."""
    # Preprocess image to match model input requirements
    img = cv2.resize(image, (width, height))
    # Add batch dimension and convert to float32 (assuming standard model)
    input_data = np.expand_dims(img, axis=0).astype(np.float32) 
    # Normalize if your model requires it (e.g., / 255.0)
    
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    
    output_data = interpreter.get_tensor(output_details[0]['index'])
    # Assuming output is probabilities like [prob_healthy, prob_unhealthy]
    predicted_index = np.argmax(output_data[0])
    confidence = output_data[0][predicted_index]
    return predicted_index, confidence

# --- 4. Main Loop ---
print("Starting sorter...")
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Optional: Add logic here to only run inference if a seed is detected
        # in the frame, rather than running it constantly on empty space.
            
        prediction, confidence = classify_image(frame)
        
        # Let's assume index 1 is "Unhealthy"
        if prediction == 1 and confidence > 0.8:
            reject_seed()
            
        # Add a small delay to prevent rapid-fire triggering on the same seed
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Stopping...")
finally:
    cap.release()
    servo.detach()