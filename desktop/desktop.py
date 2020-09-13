import os
import pyautogui
from RPA.Images import Images


def click_image(
    imagefile: str, button: str = "left", clicks: int = 1, interval: float = 0.25
):
    """Click on the center of the given image file if it is found on the screen

    :param imagefile: click on the center of this image (filepath)
    :param button: which button to click, defaults to "left"
    :param clicks: how many times mouse is clicked, defaults to 1
    :param interval: [description], defaults to 0.25
    """
    os.environ["DISPLAY"] = ":99.0"
    match = Images().find_template_on_screen(imagefile, limit=1)
    if match:
        center = match[0].center
        pyautogui.click(
            x=center.x, y=center.y, button=button, clicks=clicks, interval=interval
        )


def press_key(key: str):
    """Press key

    :param key: string for the key to click
    """
    pyautogui.press(key)