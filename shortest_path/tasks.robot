*** Settings ***
Library  RPA.Browser
Library  utils.py
Library  Collections
Library  RPA.core.notebook
Suite Teardown  Close All Browsers

*** Keyword ***
Read Demand Table
    ${table}=  Create Dictionary
    ${name}=  Get Text  xpath://tbody[@id="demand_tbody"]/tr[1]/td[1]
    ${value}=  Get Text  xpath://tbody[@id="demand_tbody"]/tr[1]/td[2]
    Set To Dictionary  ${table}  ${name}=${value}

    FOR    ${INDEX}    IN RANGE    2    11
        ${src}=  Get Element Attribute  xpath://tbody[@id="demand_tbody"]/tr[${INDEX}]/td[1]/img  src
        ${image}=  Base64 Decode  ${src}
        ${name}=  OCR  ${image}
        ${value}=  Get Text  xpath://tbody[@id="demand_tbody"]/tr[${INDEX}]/td[2]
        Set To Dictionary  ${table}  ${name}=${value}
    END

    [Return]  ${table}

*** Keyword ***
Read Supply Table
    ${table}=  Create Dictionary
    ${name}=  Get Text  xpath://tbody[@id="supply_tbody"]/tr[1]/td[1]
    ${value}=  Get Text  xpath://tbody[@id="supply_tbody"]/tr[1]/td[2]
    Set To Dictionary  ${table}  ${name}=${value}

    FOR    ${INDEX}    IN RANGE    2    7
        ${src}=  Get Element Attribute  xpath://tbody[@id="supply_tbody"]/tr[${INDEX}]/td[1]/img  src
        ${image}=  Base64 Decode  ${src}
        ${name}=  OCR  ${image}
        ${value}=  Get Text  xpath://tbody[@id="supply_tbody"]/tr[${INDEX}]/td[2]
        Set To Dictionary  ${table}  ${name}=${value}
    END
  
    [Return]  ${table}

*** Keyword ***
Copy Paste Data
    [Arguments]  ${screen_shot}
    ${supply}=  Read Supply Table
    ${demand}=  Read Demand Table
    ${supply}=  Match  ${supply}
    ${demand}=  Match  ${demand}
    
    Input Text  //div[span[text()='Cargo Description']]/textarea  ${demand}[Cargo]
    Input Text  //div[span[text()='Ship Date']]/input  ${demand}[Shipping Date]
    
    ${urgent}=  Run Keyword and Return Status  Should Contain  ${demand}[Cargo Preference]  Urgent
    Run Keyword If  ${urgent}  Select Checkbox  //input[@value='Urgent']
    Run Keyword Unless  ${urgent}  Unselect Checkbox  //input[@value='Urgent']
    
    ${permit}=  Run Keyword and Return Status  Should Contain  ${demand}[Cargo Preference]  Premit
    Run Keyword If  ${permit}  Select Checkbox  //input[@value='Premit Required']
    Run Keyword Unless  ${permit}  Unselect Checkbox  //input[@value='Premit Required']
    
    Select Radio Button  optionsRadios  ${demand}[Ship Preference]
    
    Input Text  //div[div/h5[text()='Destination (Demand)']]/div/div/div[span[text()='Name']]/input  ${demand}[Name:]
    Input Text  //div[div/h5[text()='Destination (Demand)']]/div/div/div[span[text()='Address']]/input  ${demand}[Address 1]
    Input Text  //div[div/h5[text()='Destination (Demand)']]/div/div/div[span[text()='Address-2']]/input  ${demand}[Address 2]
    Input Text  //div[div/h5[text()='Destination (Demand)']]/div/div/div[span[text()='City']]/input  ${demand}[City]
    
    Input Text  //div[div/h5[text()='Origin (Supplier)']]/div/div/div[span[text()='Name']]/input  ${supply}[Name:]
    Input Text  //div[div/h5[text()='Origin (Supplier)']]/div/div/div[span[text()='Address']]/input  ${supply}[Address 1]
    Input Text  //div[div/h5[text()='Origin (Supplier)']]/div/div/div[span[text()='Address-2']]/input  ${supply}[Address 2]
    Input Text  //div[div/h5[text()='Origin (Supplier)']]/div/div/div[span[text()='City']]/input  ${supply}[City]
    
    Select From List By Value  //div[div/h5[text()='Destination (Demand)']]//div[label[text()='State']]/select  ${demand}[State]
    Input Text  //div[div/h5[text()='Destination (Demand)']]//div[label[text()='Zip']]/input  ${demand}[Zip Code]
    Select From List By Value  //div[div/h5[text()='Origin (Supplier)']]//div[label[text()='State']]/select  ${supply}[State]
    Input Text  //div[div/h5[text()='Origin (Supplier)']]//div[label[text()='Zip']]/input  ${supply}[Zip Code]
    
    Screen Shot  filename=output/${screen_shot}
    
    Click Button  Submit Form

    Wait Until Element is Visible  //h4[contains(text(), 'Contract')]  timeout=10
    ${contract}=  Get Text  //h4[contains(text(), 'Contract')]/span
    Input Text  //table[@id='contract_table']//input  ${contract}
    Notebook Print  Contract: ${contract}

    Click Button  Create


*** Tasks ***
Shortest Path
    Open Available Browser  http://www.rpachallenge.com/assets/shortestPath/public/shortestpath.html  maximized=True
    Click Button  Start
    
    FOR    ${INDEX}    IN RANGE    1    6
        Wait Until Page Contains Element  //tbody[@id="demand_tbody"]  timeout=999
        Wait Until Page Contains Element  //tbody[@id="supply_tbody"]  timeout=999

        Copy Paste Data  round_${INDEX}.png

        Wait Until Page Does Not Contain Element  //tbody[@id="demand_tbody"]  timeout=10
        Wait Until Page Does Not Contain Element  //tbody[@id="supply_tbody"]  timeout=10
    END

    Screen Shot  filename=output/summary.png



