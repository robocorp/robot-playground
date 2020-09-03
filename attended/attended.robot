*** Settings ***
Library   Attended.py

*** Tasks ***
Attended run
    # Starting attended run
    &{response}   Request Response  questionform.json
    Log Many   ${response}