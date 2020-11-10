import pytesseract
import cv2
import base64
from PIL import Image
import regex
import numpy as np
from tempfile import NamedTemporaryFile
import json


# +
def base64_decode(text):
    # text = "data:image/png;base64,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"
    if "base64," in text:
        text = text.split("base64,", 1)[1]
    b = base64.urlsafe_b64decode(text)
    with NamedTemporaryFile(mode='w+b', suffix=".png", delete=False) as f:
        f.write(b)

    img = cv2.imread(f.name, cv2.IMREAD_UNCHANGED)
    if img.shape[2] == 4: # we have an alpha channel
        a1 = ~img[:, :, 3] # extract and invert that alpha
        img = cv2.add(cv2.merge([a1, a1, a1, a1]), img) # add up values (with clipping)
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY) # strip alpha channel

    return despeckle(img)

def ocr(image):
    image = cv2.resize(image, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
    return pytesseract.image_to_string(image).strip()



# +
def bare(value):
    return "".join([x for x in value if x.isalnum()]).lower()

# error function is levenshtein distance divided by length of correct string
def error(candidate, target):
    candidate, target = bare(candidate), bare(target)
    error = sum(regex.fullmatch(r"(?b)(%s){e}" % candidate, target).fuzzy_counts)
    return float(error) / len(target)

DEMAND = ["Name:", "Shipping Date", "State", "City", "Address 1", "Address 2", 
             "Zip Code", "Cargo Preference", "Cargo", "Ship Preference"]
SUPPLY = ["Name:", "State", "City", "Address 1", "Address 2", "Zip Code"]

def match(table):
    real_names = (DEMAND if len(table) == len(DEMAND) else SUPPLY).copy()
    nick_names = list(table.keys())

    matches = []
    for nick in nick_names:
        for real in real_names:
            matches.append((error(nick, real), real, nick))

    results = {}    
    for err, real, nick in sorted(matches):
        if real in real_names and nick in nick_names:
            results[real] = table[nick]
            real_names.remove(real)
            nick_names.remove(nick)

    return results



# +
BLACK, WHITE = 0, 255

def floodfill(image, x, y, min_size, area=None):
    if area is None:
        area = []
    if image[y][x] == BLACK:
        image[y][x] = WHITE
        area.append((x, y))
        if len(area) == min_size:
            for x, y in area:
                image[y][x] = BLACK
            return area

        if x > 0:
            floodfill(image, x-1, y, min_size, area)
            if len(area) == min_size:
                return area
        if x < image.shape[1] - 1:
            floodfill(image, x+1, y, min_size, area)
            if len(area) == min_size:
                return area
        if y > 0:
            floodfill(image, x, y-1, min_size, area)
            if len(area) == min_size:
                return area
        if y < image.shape[0] - 1:
            floodfill(image, x, y+1, min_size, area)
            if len(area) == min_size:
                return area

    return area

def despeckle(img, min_size=5, threshold=164):
    h, w = img.shape

    # binarization with threshold of 164
    for y in range(h):
        for x in range(w):
            if img[y, x] < threshold:
                img[y, x] = BLACK
            else:
                img[y, x] = WHITE

    # floodfill :) to remove area<5 pixel masses
    for y in range(h):
        for x in range(w):
            floodfill(img, x, y, min_size)

    return img
# -


