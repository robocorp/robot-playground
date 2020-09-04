*** Settings ***
Documentation  Sends message to Slack channel
...  %PATH
...  %MESSAGE
...  %SECRET .WEBHOOK
...  %CHANNEL
Library  OperatingSystem
Library  RPA.Robocloud.Secrets
Library  RPA.Robocloud.Items
Library  RPA.Notifier

*** Keyword ***
Send by Message
    ${message}=  Get Environment Variable  SLACK_MESSAGE
    Send Message  ${message}


*** Keyword ***
Send by Path
    ${path}=  Get Environment Variable  SLACK_PATH
    ${message}=  Get Work Item Variable  ${path}
    Send Message  ${message}


*** Keyword ***
Send Message
    [Arguments]    ${message}
    ${secrets}=  Get Secret  %{SLACK_SECRET}
    Notify Slack  ${message}  channel=%{SLACK_CHANNEL}  webhook_url=${secrets}[WEBHOOK]

*** Task ***
Send Message to Slack Channel
    ${exists}=  Run Keyword and Return Status  Get Environment Variable  SLACK_MESSAGE
    Run Keyword If  ${exists}  Send by Message

    ${exists}=  Run Keyword and Return Status  Get Environment Variable  SLACK_PATH
    Run Keyword If  ${exists}  Send by Path
    
    Log  You must specify SLACK_MESSAGE or SLACK_PATH environment variable
