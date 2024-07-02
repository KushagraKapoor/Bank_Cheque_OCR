import cv2
import os
def signature(image_path, save_path):
    img = cv2.imread(image_path)

    cv2.imwrite(save_path, img)
    return save_path


def detect_signature(image_path):
    # Read the image
    
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image = image[600:950, 1720:2320]
    if image is None:
        return False

    # Apply a binary threshold to the image to create a binary image
    _, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Find contours in the binary image
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter out small contours that are unlikely to be signatures
    min_contour_area = 1000  # Adjust this threshold based on your requirements
    signature_contours = [contour for contour in contours if cv2.contourArea(contour) > min_contour_area]

    # If there are any contours left, we assume there is a signature
    if len(signature_contours) > 0:
        return True
    else:
        return False
