import pytesseract
import cv2
import numpy as np
import os

def process_math_scan(image_path):
    """
    Processes an image scan containing mathematical formulas or text using OCR.
    Handles adaptive thresholding to remove shadows and enhance contrast for better extraction.
    """
    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at path: {image_path}")

        # 1. Load and Grayscale
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"OpenCV could not read the image: {image_path}")
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 2. Adaptive Thresholding (Handles shadows on paper)
        processed_img = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        # 3. OCR Extraction
        # 'config' is tuned for mathematical symbols (--psm 6 assumes a single uniform block of text)
        extracted_text = pytesseract.image_to_string(processed_img, config='--psm 6')
        
        return extracted_text.strip()
        
    except Exception as e:
        print(f"[OCR ERROR] Failed to process math scan: {e}")
        return ""
