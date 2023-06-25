import albumentations as A
from albumentations.pytorch import ToTensorV2
import albumentations.augmentations as AA
import os
import numpy
import cv2
from torchvision import transforms
from PIL import Image

# Path to the directory containing the images
image_dir = 'D:/yolo/valid/images'

# Path to the directory containing the annotation files
annotation_dir = 'D:/yolo/valid/labels'

# Define the transformations
transform = A.Compose([
    A.Downscale(scale_min=0.5, scale_max=0.8, interpolation=cv2.INTER_LINEAR),
    A.RGBShift(),
    A.Blur(),
    A.GaussNoise(),
    A.CoarseDropout(max_holes=40, max_height=64, max_width=64),
    A.RandomBrightnessContrast(),
    ToTensorV2()
])

# Loop through each image and its corresponding annotation file
for image_file in os.listdir(image_dir):
    if image_file.endswith('.jpg'):
        image_path = os.path.join(image_dir, image_file)
        annotation_file = image_file.replace('.jpg', '.txt')
        annotation_path = os.path.join(annotation_dir, annotation_file)

        # Load the image and the annotation file
        image = numpy.array(Image.open(image_path))
        annotation_data = open(annotation_path).readlines()

        # Save the augmented image
        augmented_image = transform(image=image)['image']
        # Convert the augmented image tensor to a PIL Image object
        augmented_image_pil = transforms.ToPILImage()(augmented_image)
        augmented_image_pil.save('D:/yolo_aug/valid/images/' + image_file)

        # Update the annotation file with the transformed bounding box coordinates
        with open('D:/yolo_aug/valid/labels/' + annotation_file, 'w') as f:
            for line in annotation_data:
                class_label, x, y, width, height = line.strip().split()
                transformed_coords = [x, y, width, height]  # Use the original coordinates since 'augmented_image' doesn't have 'bbox' attribute
                transformed_coords = [str(coord) for coord in transformed_coords]
                f.write(f'{class_label} {" ".join(transformed_coords)}\n')