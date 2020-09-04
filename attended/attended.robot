*** Settings ***
Library   Attended.py

*** Keywords ***
Request By Form Constructed With Keywords
    ${options}          Create List   red  blue  green
    Create Form         My custom form
    Add Text Input      What is your name   name
    Add Dropdown        Select your color   color   ${options}  green
    Add Dropdown        Select your job     job     engineer,manager,technician
    Add Submit          myselection     yes,no
    &{response}         Request Response
    Log Many            ${response}

Request By Form Defined With JSON
    &{response}         Request Response  questionform.json
    Log Many            ${response}

*** Tasks ***
Attending
    Request By Form Constructed With Keywords
    Request By Form Defined With JSON
