

# import the necessary packages
from pytesseract import Output
from blur_and_threshold import blur_and_threshold
import pytesseract
import cv2
import imutils
from PIL import ImageFont, ImageDraw, Image
import numpy as np

# construct the argument parser and parse the arguments
def containsNumber(value):
    for character in value:
        if character.isdigit():
            return True
    return False


def ocr_cccd(image):
# load the input image, convert it from BGR to RGB channel ordering,
# and use Tesseract to localize each area of text in the input image
    image = imutils.resize(image, width=800)
    image1 = image.copy()
    image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    options = "-l vie7 --psm 11"
    options1 = "-l vie5 -c tessedit_char_whitelist=0123456789 --psm 11"

    final = blur_and_threshold(gray)
    number = pytesseract.image_to_string(final, config=options1)
    number = number.replace("\n\x0c", "")
    number = number.replace("\n", " ")
    x = number.split(" ")
    for i in x:
        if len(i) > 10:
            number = i

    results = pytesseract.image_to_data(final, config=options, output_type=Output.DICT)

    # loop over each of the individual text localizations
    for i in range(0, len(results["text"])):


        # extract the bounding box coordinates of the text region from the current result
        x = results["left"][i]
        y = results["top"][i]
        w = results["width"][i]
        h = results["height"][i]



        # extract the OCR text itself along with the confidence of the text localization
        text = results["text"][i]
        conf = int(results["conf"][i])

        # filter out weak confidence text localizations
        if conf > 40:
            if (y / image.shape[0])<0.4 and containsNumber(text):

                if len(number) ==12:
                    text = number

            # display the confidence and text to our terminal
            print("Confidence: {}".format(conf))
            print("Text: {}".format(text))
            print("")
            cv2.rectangle(image1, (x, y), (x + w, y + h), (0, 255, 0), 2)

            fontpath = "./BeVietnam-Medium.ttf"
            font = ImageFont.truetype(fontpath, 18)
            image1 = Image.fromarray(image1)
            draw = ImageDraw.Draw(image1)
            draw.text((x + 10, y - 30), text, font=font, fill=(0, 0, 255))
            image1 = np.array(image1)

# show the output image
    cv2.imshow("Image", imutils.resize(image1, width=700))
    cv2.waitKey(0)


