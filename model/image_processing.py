import pytesseract
import cv2

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# may need to update the path to the location of tesseract executable on your machine

def remove_line(image):
        removed = image.copy()
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        
        # Remove vertical lines
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,40))
        remove_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
        cnts = cv2.findContours(remove_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            cv2.drawContours(removed, [c], -1, (255,255,255), 15)

        # Remove horizontal lines
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40,1))
        remove_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
        cnts = cv2.findContours(remove_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            cv2.drawContours(removed, [c], -1, (255,255,255), 5)

        # Repair kernel
        repair_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
        removed = 255 - removed
        dilate = cv2.dilate(removed, repair_kernel, iterations=5)
        dilate = cv2.cvtColor(dilate, cv2.COLOR_BGR2GRAY)
        pre_result = cv2.bitwise_and(dilate, thresh)

        result = cv2.morphologyEx(pre_result, cv2.MORPH_CLOSE, repair_kernel, iterations=5)
        final = cv2.bitwise_and(result, thresh)

        invert_final = 255 - final
        
        normal_image = cv2.cvtColor(invert_final,cv2.COLOR_GRAY2BGR)
        return normal_image

def pre_processing(image):
        # convert the image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Apply thresholding to create a binary image
        threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[-1]
        return threshold_img

def extract_text_from_image(image_path):
        # Read the image file and Rrmove the horizontal and vertical lines from it
        image = cv2.imread(image_path)
        image = remove_line(image)

        # Threshold the image to create a binary image
        threshold_img = pre_processing(image)

        # Pass image to tesseract with appropriate parameters
        tesseract_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(threshold_img, config=tesseract_config, lang='Vietnamese')
        return text