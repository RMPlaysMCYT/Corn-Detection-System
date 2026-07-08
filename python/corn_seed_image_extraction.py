import cv2
import numpy as np
import os

def_split_corn_seed_images(input_directory, output_directory, num_splits, prefix="corn_seed"):
    """
    Splits corn seed images into multiple parts and saves them in the output directory.

    Parameters:
    - input_directory: str, path to the directory containing the original images.
    - output_directory: str, path to the directory where split images will be saved.
    - num_splits: int, number of parts to split each image into.
    - prefix: str, prefix for the output filenames (default is "corn_seed").
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(input_directory):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            img_path = os.path.join(input_directory, filename)
            img = cv2.imread(img_path)

            height, width, _ = img.shape
            split_width = width // num_splits

            for i in range(num_splits):
                start_x = i * split_width
                end_x = (i + 1) * split_width if i < num_splits - 1 else width
                split_img = img[:, start_x:end_x]

                output_filename = f"{prefix}_{os.path.splitext(filename)[0]}_part{i + 1}.jpg"
                output_path = os.path.join(output_directory, output_filename)
                cv2.imwrite(output_path, split_img)