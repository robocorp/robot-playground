*** Settings ***
Library   desktop.py

*** Tasks ***
Open Ubuntu menu
  Click Image   ubuntumenu.png
  Sleep   5s
  Press Key     esc
