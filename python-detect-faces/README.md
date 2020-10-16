# python-detect-faces

This Python based robot downloads an image from Google based on search term
and detects faces in it.

If faces are detected, bounding boxes are drawn to the image together with the
count of detected faces. Face detection is based on Haar feature-based cascade classifier
and it runs locally (not using external cloud services), as enabled by opencv-python.

Downloaded image is stored as `output/screenshot.png` and the bounding boxes are
shown in `output/screenshot-faces.png`.
