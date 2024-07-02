import cv2
import re
from .models import CheckData
from paddleocr import PaddleOCR, draw_ocr
import matplotlib.pyplot as plt
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)  # use_gpu=False for CPU usage

def extract_ifsc_gb(image_path):
    image = cv2.imread(image_path)
    roi_start_y, roi_start_x = 0, 0
    roi_height, roi_width = 350, 650
    img_micr = image[roi_start_y:roi_start_y + roi_height, roi_start_x:roi_start_x + roi_width]
    result = ocr.ocr(img_micr, cls=True)
    text = " ".join([line[1][0] for line in result[0]])
    text = text.replace("O", "0") 
    text = text.replace("$", "S") 
    ifsc_pattern = r'\b[A-Z]{4}[\d]{7}|[A-Z]{4}[\d]{6}|[A-Z]{4}[\d]{8}|[I][C][I][C][\d]{7}\b|[C][N][R][B]{7}|[C][N][R][B][\d]{6} [\d]{1}|[C][N][\d][B][\d]{7}|[C][N][R][B][\d]{7}|[S][Y][N][B]\d{7}|[S][Y][N][B][\d]{6} [\d]{1}|[U][T][Ili][B][O0]\d{6}\b|[U][T][I][B][\d]{6} [\d]{1}'  # Adjust
    ifsc_match = re.search(ifsc_pattern, text)
    if ifsc_match:
        return ifsc_match.group()
    else:
        return None

def extract_account_no_gb(image_path):
    image = cv2.imread(image_path)
    image = image[300:900, 200:1100]
    result = ocr.ocr(image, cls=True)
    text = " ".join([line[1][0] for line in result[0]])
    account_no_pattern = r'[\d]{12}|[\d]{11} [\d]{1}|[$][\d]{11}|[\d]{13}|[\d]{12} [\d]{1}|[$][\d]{12}|[\d]{14}|[\d]{13} [\d]{1}|[$][\d]{13}|[\d]{15}'
    acc_match = re.search(account_no_pattern, text)
    if acc_match:
        return acc_match.group()
    else:
        return None


def micr_account_no(image_path):
    
 img = cv2.imread(image_path)
 height, width, _ = img.shape
 bottom_height = 150
 img_bottom = img[height - bottom_height:height, :]
 img_rgb = cv2.cvtColor(img_bottom, cv2.COLOR_BGR2RGB)
 rea = pytesseract.image_to_string(img_rgb, lang='mcr')
 chkno=rea[1:7]
 micr_code=rea[9:18]


import cv2
from paddleocr import PaddleOCR, draw_ocr
import matplotlib.pyplot as plt

# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)  # use_gpu=False for CPU usage

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    normalized_img = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)  # Normalize the image
    return normalized_img

def hand_name_gb(image_path):
    img = cv2.imread(image_path)
    img = img[190:340, 150:1700]
    preprocessed_img = preprocess_image(img)
    result = ocr.ocr(preprocessed_img, cls=True)
    txts = [line[1][0] for line in result[0]]
    string1 = " ".join(txts)
    return string1

def amount_gb(image_path):
    img = cv2.imread(image_path)
    img = img[320:550, 1800:2500]
    preprocessed_img = preprocess_image(img)
    result = ocr.ocr(preprocessed_img, cls=True)
    txts = [line[1][0] for line in result[0]]
    string2 = " ".join(txts)
    return string2

def amount_in_numbers_gb(image_path):
    img = cv2.imread(image_path)
    img = img[297:450, 350:2200]
    result = ocr.ocr(img)
    plt.imshow(img)
    txts=[line[1][0] for line in result[0]]
    string3=" ".join(txts)

    return string3
