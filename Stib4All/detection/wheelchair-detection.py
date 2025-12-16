import os
from pathlib import Path
from ultralytics import YOLO
import torch
import yaml
from PIL import Image
import shutil


def load_image(path):
    test_image = Image.open(path)
    return test_image

def evaluate_image(image):
    model = YOLO("wheelchair-model.pt")
    results = model(image)
    for result in results:
        boxes = result.boxes  # Boxes object for bounding box outputs
        masks = result.masks  # Masks object for segmentation masks outputs
        keypoints = result.keypoints  # Keypoints object for pose outputs
        probs = result.probs  # Probs object for classification outputs
        obb = result.obb  # Oriented boxes object for OBB outputs
        print(f"Number of wheelchairs detected : {len(boxes)}")
        #result.show()  # display to screen
        result.save(filename="result.jpg")  # save to disk

if __name__ == "__main__":
    image = load_image("input_images/test/test2.jpg")
    evaluate_image(image)