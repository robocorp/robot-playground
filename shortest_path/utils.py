import pytesseract
import cv2
import base64
import regex
from tempfile import NamedTemporaryFile
import json


# +
def base64_decode_image(text):
    if "base64," in text:
        text = text.split("base64,", 1)[1]
    b = base64.urlsafe_b64decode(text)
    with NamedTemporaryFile(mode='w+b', suffix=".png", delete=False) as f:
        f.write(b)

    img = cv2.imread(f.name, cv2.IMREAD_UNCHANGED)
    if img.shape[2] == 4:  # we have an alpha channel
        a1 = ~img[:, :, 3]  # extract and invert that alpha
        img = cv2.add(cv2.merge([a1, a1, a1, a1]), img)  # add up values (with clipping)
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)  # strip alpha channel

    return img

def ocr(image):
    return pytesseract.image_to_string(image).strip()



# +
def bare(value):
    return "".join([x for x in value if x.isalnum()]).lower()

# error function is levenshtein distance divided by length of correct string
def error(candidate, target):
    candidate, target = bare(candidate), bare(target)
    error = sum(regex.fullmatch(r"(?b)(%s){e}" % candidate, target).fuzzy_counts)
    return float(error) / len(target)


def match(table, names):
    names = list(names)
    values = list(table.keys())

    matches = []
    for value in values:
        for name in names:
            matches.append((error(value, name), name, value))

    results = {}
    for err, name, value in sorted(matches):
        if name in names and value in values:
            results[name] = table[value]
            names.remove(name)
            values.remove(value)

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

def despeckle_image(img, min_size=5, threshold=164):
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

def resize_image(image, scale):
    scale = float(scale)
    return cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

# -


