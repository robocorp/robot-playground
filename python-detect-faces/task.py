# Robot will search for an image in Google and detect faces in it
# using Haar feature-based cascade classifier.
#
# Ref: https://techtutorialsx.com/2017/05/02/python-opencv-face-detection-and-counting/

from RPA.Browser import Browser
import cv2

# +
# Search term used in Google
term = "ac/dc band members"

url = "https://images.google.com"
screenshot_filename = "output/screenshot.png"
bbox_filename = "output/screenshot-faces.png"
face_cascade = cv2.CascadeClassifier("./haarcascade_frontalface_default.xml")
browser = Browser()


# -

def open_the_website(url: str):
    browser.open_available_browser(url)


def search_for(term: str):
    input_field = "name:q"
    browser.input_text(input_field, term)
    browser.press_keys(input_field, "ENTER")


def store_screenshot(filename: str):
    browser.capture_element_screenshot("css:div[data-ri=\"0\"]", filename=filename)


def faces_found_in_image(filename: str, bbox_filename: str):
    """ Return number of faces detected at file.
        Draw detected face bounding boxes to bbox_filename.
    """

    original = cv2.imread(filename)
    gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)
    if len(faces) == 0:
        return None

    if bbox_filename:
        for (x,y,w,h) in faces:
            cv2.rectangle(original, (x,y), (x+w,y+h), (0,255,0), 1)

            cv2.rectangle(original, ((0,original.shape[0] -25)),(270, original.shape[0]), (255,255,255), -1)
            cv2.putText(original, "Faces: " + str(faces.shape[0]), (0,original.shape[0] -10), cv2.FONT_HERSHEY_TRIPLEX, 0.5,  (0,0,0), 1)
            cv2.imwrite(bbox_filename, original)

    return faces.shape[0]


def main():
    try:
        open_the_website(url)
        search_for(term)
        store_screenshot(screenshot_filename)
        hits = faces_found_in_image(screenshot_filename, bbox_filename)
        if hits:
            print("Detected {} faces in {}".format(hits, bbox_filename))
        else:
            print("No faces detected")
    finally:
        browser.close_all_browsers()


if __name__ == "__main__":
    main()


