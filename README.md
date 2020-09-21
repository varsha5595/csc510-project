# <img src="./resources/benten.png" height="42" width="42"/> Sync Ends Slack Bot

## End development overheads (out of the box `slack-bot` support for `Github` and `Postman`)

Software Engineering Project for CSC 510 Fall 20

[![Support Slack](https://img.shields.io/badge/support-slack-red.svg)](https://join.slack.com/t/seng20/shared_invite/zt-hmikwiec-KDQVndRqN5DvGEFql0ehIw)
[![License](https://img.shields.io/github/license/intuit/benten.svg)](https://github.com/varsha5595/csc510-project)

Sync Ends is an automated bridge to sync service owners and service consumers. Every team has a single postman collection that they use to test their APIs and share it across in their documentations. The backend team has to register their service on our application and we take care of the rest. Everytime there is a change in the way the api is called, we parse the changes and inform the consumers. This way all the team members are informed about the changes and know exactly what to edit in their product. The [Slack](https://slack.com/) framework lets you concentrate on the `core` functionality you want to build without worrying about integration overheads.

[![Watch the video](https://github.com/varsha5595/csc510-project/blob/master/etc/thumbnail.PNG)](https://youtu.be/SeNdRiI1axA)

## Features
|Feature|Description  |
|--|--|
|API Change Notification  |```Changes made to the API in postman```
|API Changes  |```Automated detailed diff of the changes```|
|Slack Bot Subscription   |```Subscribe to a list of APIs based on your preference``` , ``` Set frequency and method of update``` |
|Configurable Ping |```Choose the ping interval to detect changes in a collection```  |
|Testing  |```Polling service to test API uptime```  |
|API history and change logs  |```Tracking the list of changes all the way from V1```  |
| | |


# Start Sync Ends
```sh
python3 server.py
```
In line #69 replace `<slackbot token>` with your bot token after bot creation: [Creating Slack Bot](https://github.com/varsha5595/csc510-project/wiki)
