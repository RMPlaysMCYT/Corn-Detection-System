import cv2, time

print("OpenCV:", cv2.__version__)

for idx in range(4):
    cap = cv2.VideoCapture(idx)
    print(f"\n--- index {idx}: isOpened={cap.isOpened()} ---")
    if cap.isOpened():
        for i in range(15):
            ret, frame = cap.read()
            print(f"  read {i:02d}: ret={ret}, "
                  f"frame={'None' if frame is None else frame.shape}")
            if ret and frame is not None and i == 14:
                cv2.imwrite(f"cam_{idx}.png", frame)
                print(f"  saved cam_{idx}.png")
            time.sleep(0.1)
    cap.release()