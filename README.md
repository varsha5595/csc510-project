# <img src="./etc/bot.png" height="42" width="42"/> Sync Ends

## End development overheads

Software Engineering Project for CSC 510

[![Support Slack](https://img.shields.io/badge/support-slack-red.svg)](https://join.slack.com/t/seng20/shared_invite/zt-hmikwiec-KDQVndRqN5DvGEFql0ehIw)
[![Build Status](https://travis-ci.com/varsha5595/csc510-project.svg?branch=master)](https://travis-ci.com/varsha5595/csc510-project)
[![DOI](https://zenodo.org/badge/292436508.svg)](https://zenodo.org/badge/latestdoi/292436508)

Sync Ends is an automated bridge to sync service owners and service consumers. Every team has a single postman collection that they use to test their APIs and share it across in their documentations. The backend team has to register their service on our application and we take care of the rest. Everytime there is a change in the way the api is called, we parse the changes and inform the consumers. This way all the team members are informed about the changes and know exactly what to edit in their product. The [Slack](https://slack.com/) framework lets you concentrate on the `core` functionality you want to build without worrying about integration overheads.

[![Watch the video](https://github.com/varsha5595/csc510-project/blob/master/etc/thumbnail.PNG)](https://youtu.be/SeNdRiI1axA)

# Architecture Diagram
<img src="./etc/architecture.PNG" height="500" width="800"/>

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
