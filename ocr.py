# import libraries
import csv
import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def remove_line(image):
    # image = cv2.imread('image2 (1).png')
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
    cv2.imshow("final",normal_image)
    cv2.waitKey()
    return normal_image

def pre_processing(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # converting it to binary image
    threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[-1]
    # saving image to view threshold image
    cv2.imwrite('thresholded.png', threshold_img)
    cv2.imshow('threshold image', threshold_img)
    # Maintain output window until
    # user presses a key
    cv2.waitKey(0)
    # Destroying present windows on screen
    cv2.destroyAllWindows()

    return threshold_img


def parse_text(threshold_img):
    tesseract_config = r'--oem 3 --psm 6'
    details = pytesseract.image_to_data(threshold_img, output_type=pytesseract.Output.DICT,
                                        config=tesseract_config, lang='Vietnamese')
    return details


def draw_boxes(image, details, threshold_point):
    total_boxes = len(details['text'])
    for sequence_number in range(total_boxes):
        if int(details['conf'][sequence_number]) >= threshold_point:
            (x, y, w, h) = (details['left'][sequence_number], details['top'][sequence_number],
                            details['width'][sequence_number], details['height'][sequence_number])
            image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # saving image to local
    cv2.imwrite('captured_text_area.png', image)
    # display image
    cv2.imshow('captured text', image)
    # Maintain output window until user presses a key
    cv2.waitKey(0)
    # Destroying present windows on screen
    cv2.destroyAllWindows()


def format_text(details):
    parse_text = []
    word_list = []
    last_word = ''
    for word in details['text']:
        if word != '':
            word_list.append(word)
            last_word = word
        if (last_word != '' and word == ' ') or (word == details['text'][1]):
            parse_text.append(word_list)
            word_list = []

    return parse_text


def write_text(formatted_text):
    with open('resulted_text.txt', 'w', encoding='utf8', newline='') as file:
        csv.writer(file, delimiter=" ").writerows(formatted_text)


if __name__ == "__main__":
    # reading image from local
    image = cv2.imread('image4.png')
    #calling remove_line function to remove all border of the original image
    borderless_image = remove_line(image) 
    # calling pre_processing function to perform pre-processing on input image.
    thresholds_image = pre_processing(borderless_image)
    # calling parse_text function to get text from image by Tesseract.
    parsed_data = parse_text(thresholds_image)
    # defining threshold for draw box
    accuracy_threshold = 30
    # calling draw_boxes function which will draw dox around text area.
    draw_boxes(thresholds_image, parsed_data, accuracy_threshold)
    # calling format_text function which will format text according to input image
    arranged_text = format_text(parsed_data)
    # calling write_text function which will write arranged text into file
    write_text(arranged_text)