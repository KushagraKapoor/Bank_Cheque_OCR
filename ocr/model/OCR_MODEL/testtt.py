import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

from PIL import Image
import re

def preprocess_image(image_path):
    # Load the image
    image = cv2.imread(image_path)
  
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply thresholding for better OCR results
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    return thresh

def extract_text(image):
    # Perform OCR on the image
    text = pytesseract.image_to_string(image)
    return text

def extract_information(text):
    # Extract relevant information using regular expressions or keyword searches
    info = {}

    # Example regex patterns for extracting cheque details
    cheque_number_pattern = re.compile(r'Cheque Number:?\s*(\d+)')
    date_pattern = re.compile(r'Date:?\s*(\d{2}/\d{2}/\d{4})')
    payee_pattern = re.compile(r'Pay to the Order of:? (.+)')
    amount_pattern = re.compile(r'(\d+,\d+\.\d{2}|\d+\.\d{2})')

    # Extract using regex
    cheque_number = cheque_number_pattern.search(text)
    date = date_pattern.search(text)
    payee = payee_pattern.search(text)
    amount = amount_pattern.search(text)

    if cheque_number:
        info['Cheque Number'] = cheque_number.group(1)
    if date:
        info['Date'] = date.group(1)
    if payee:
        info['Payee'] = payee.group(1).strip()
    if amount:
        info['Amount'] = amount.group(1)

    return info

def check_signature(image):
    # Assuming the signature is in the bottom right corner of the cheque
    height, width = image.shape
    signature_region = image[int(height*0.7):height, int(width*0.6):width]

    # Perform OCR on the signature region
    signature_text = pytesseract.image_to_string(signature_region)

    # Check for presence of signature
    return bool(signature_text.strip())

def main():
    cheque_image_path = 'cheque.jpeg'
    image = preprocess_image(cheque_image_path)
    text = extract_text(image)
    info = extract_information(text)
    signature_present = check_signature(image)

    # Display the results
    print("Extracted Information:")
    for key, value in info.items():
        print(f"{key}: {value}")
    
    print("\nSignature Present:", signature_present)

if __name__ == "__main__":
    main()
