*** Settings ***
Library   Collections
Library   OperatingSystem
Library   RPA.Browser
Library   RPA.Cloud.Google  robocloud_vault_name=google
...                        robocloud_vault_secret_key=service_account
Library   RPA.Excel.Files
Library   RPA.Notifier
Library   RPA.Robocloud.Items
Library   RPA.Robocloud.Secrets
Library   RPA.Tables

*** Keywords ***
Get Info From CRM
    [Arguments]  ${name}
    Open Workbook   userdata.xlsx
    ${profiles}     Read Worksheet As Table  name=profile  header=True
    Filter table by column    ${profiles}    name  ==  ${name}
    ${address}=	    Get Address From Profile    ${profiles}
    [Return]  ${address}

Get Address From Profile
    [Arguments]     ${profiles}
    ${len}=         Get Length    ${profiles}
    ${profile}      Run Keyword If  ${len} == 1  Pop Table Row    ${profiles}
    ${address}=	    Set Variable If	${len} == 1  ${profile}[address]   UNKNOWN
    [Return]        ${address}

Get Feedback Sentiment
    [Documentation]  Return relatively text positive score, and relatively emotional magnitude
    [Arguments]  ${text}
    Init Natural Language Client    use_robocloud_vault=True
    Create File   analysistext.txt   ${text}
    ${result}=    Analyze Sentiment    analysistext.txt
    [Return]     ${result.document_sentiment}

Input data into form
    [Arguments]  ${name}   ${text}
    Input Text   ${FORM_NAME_FIELD}  ${name}
    Input Text   ${FORM_TEXT_FIELD}  ${text}
    Submit Form  ${FORM_LOCATOR}
    Wait Until Page Contains Element    css:.alert-success   timeout=15s

Teardown for feedback form
    Close Workbook
    Close All Browsers

Check types for score and user
    [Arguments]  ${sentiment}  ${address}
    ${score}            Convert To Number   ${sentiment}   1
    ${score_type}=      Set Variable If
    ...                 ${score} < -0.2  Negative
    ...                 ${score} > 0.2   Positive
    ${score_type}=      Set Variable If  "${score_type}" == "None"  Neutral   ${score_type}
    ${user_type}=       Set Variable If  """${address}""" == "UNKNOWN"  external user  customer in crm
    [Return]  ${score_type}  ${score}  ${user_type}