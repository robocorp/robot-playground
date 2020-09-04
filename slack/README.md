# Slack Notifier

Reusable Robot that can send notifications to Slack channel

Environment variables:

| Environment variable  | Usage |
| ------------- | ------------- |
| SLACK_PATH or SLACK_MESSAGE | Use either SLACK_PATH or SLACK_MESSAGE. SLACK_MESSAGE defines the notification message. SLACK_PATH defines the Robocorp work item's key that contains the message.  |
| SLACK_CHANNEL  | Slack channel name  |
| SLACK_SECRET  | Name of Robocorp vault's secret that holds the Slack webhook in key WEBHOOK |

