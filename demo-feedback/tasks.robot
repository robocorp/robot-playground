*** Settings ***
Resource  keywords.robot
Resource  variables.robot

*** Tasks ***
Process Feedback From Excel
    [Documentation]  Read feedback rows from Excel, input them into web form and submit.
    Open Workbook             userdata.xlsx
    Open Available Browser    ${FORM_URL}
    @{worksheet}=             Read worksheet  name=feedback  header=${TRUE}
    Input data into form  Random User   I am really delighted to give you feedback
    FOR  ${row}  IN  @{worksheet}
        Input data into form  ${row}[name]   ${row}[feedback]
    END
    Input data into form  John Doe  This was a nice experience
    [Teardown]  Teardown for feedback form

Analyze Feedback
    [Documentation]  Do sentiment analysis for received text and find name from CRM.
    ${secrets}          Get Secret  google
    Init Sheets Client  use_robocloud_vault=True
    ${payload}          Get Work Item Payload
    ${address}          Get Info From CRM       ${payload}[variables][name]
    ${sentiment}        Get Feedback Sentiment  ${payload}[variables][message]
    ${timestamp}        Get Time  UTC
    @{values}           Create List    ${timestamp}  ${payload}[variables][name]  ${address}  ${payload}[variables][message]  ${sentiment.score}
    Insert Values       ${SHEET_ID}  ${SHEET_RANGE}  ${values}
    ${score_type}  ${score}  ${user_type}=  Check types for score and user  ${sentiment.score}  ${address}
    Notify Slack        ${score_type}(${score}) feedback from *${payload}[variables][name]* (${user_type}) received.   \#robotsparebin-industries   ${secrets}[slack_hook]

Process analyzed feedbacks
    [Documentation]  Gather all feedback from Google Sheets and make summary. Post to Slack and archive feedbacks.
    ${secrets}          Get Secret  google
    Init Sheets Client  use_robocloud_vault=True
    ${res}              Get Values   ${SHEET_ID}  feedback!A1:E1500
    ${table}            Create Table  ${res}[values]
    ${header}=          Pop table row    ${table}    as_list=${TRUE}
    ${feedback_count}   Get Length  ${table}
    Pass Execution If   ${feedback_count} == 0  Nothing to analyze in the Google Sheets
    Rename table columns    ${table}    ${header}
    &{summary}          Create Dictionary  in_crm=${0}  external=${0}  positive=${0}  neutral=${0}  negative=${0}
    FOR   ${row}   IN   @{table}
        Run Keyword If       """${row}[Address]""" == "UNKNOWN"   Set To Dictionary   ${summary}   external=${summary.external+1}
        Run Keyword Unless   """${row}[Address]""" == "UNKNOWN"   Set To Dictionary   ${summary}   in_crm=${summary.in_crm+1}
        Run Keyword If       ${row}[Sentiment] < -0.2   Set To Dictionary   ${summary}   negative=${summary.negative+1}
        Run Keyword If       ${row}[Sentiment] > 0.2   Set To Dictionary   ${summary}   positive=${summary.positive+1}
        @{row_as_list}   Evaluate   list(${row}.values())
        Insert Values    ${SHEET_ID}    archive!A2:E1500   ${row_as_list}
    END
    Set To Dictionary   ${summary}   neutral=${${feedback_count}-${summary.positive}-${summary.negative}}
    Notify Slack        *RobotSpareBin Industries feedback summary*\nTotal number of feedbacks: ${feedback_count}\nAnalyzed as positive: ${summary.positive}\nAnalyzed as neutral: ${summary.neutral}\nAnalyzed as negative: ${summary.negative}\n\nFrom customers in our CRM: ${summary.in_crm}\nFrom external users: ${summary.external}\n   \#robotsparebin-industries   ${secrets}[slack_hook]
    Clear Values        ${SHEET_ID}  feedback!A2:E1500
