# <img src="https://github.com/jaymodi98/Sync-Ends/blob/master/images/bot.png" height="42" width="42"/> Sync Ends

## End development overheads

Software Engineering Project for CSC 510

[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
![GitHub](https://img.shields.io/badge/language-python-blue.svg)
![GitHub contributors](https://img.shields.io/github/contributors/jaymodi98/Sync-Ends)
[![Build Status](https://travis-ci.com/jaymodi98/Sync-Ends.svg?branch=master)](https://travis-ci.com/jaymodi98/Sync-Ends)
<br>
![GitHub closed issues](https://img.shields.io/github/issues-closed-raw/jaymodi98/Sync-Ends)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/jaymodi98/Sync-Ends)
[![codecov](https://codecov.io/gh/jaymodi98/Sync-Ends/branch/master/graph/badge.svg?token=DP2AWTXOXL)](undefined)<br>
[![DOI](https://zenodo.org/badge/300105279.svg)](https://zenodo.org/badge/latestdoi/300105279)
![YouTube Video Views](https://img.shields.io/youtube/views/1Pd3Enj13m8?style=social)

Sync Ends is an automated bridge to sync service owners and service consumers. Every team has a single Postman collection that they use to test their APIs and share it across in their documentations. The backend team has to register their service on our application and we take care of the rest. Everytime there is a change in the way the API is called, we parse the changes and inform the API consumers. This way all the team members are informed about the changes and know exactly what to edit in their codebase. The Slack framework lets you concentrate on the **core** functionality you want to build without worrying about integration overheads.

[![Watch the video](https://github.com/jaymodi98/Sync-Ends/blob/master/images/screenshotpromo.png)](https://www.youtube.com/watch?v=1Pd3Enj13m8)

# Architecture Diagram
<img src="https://github.com/jaymodi98/Sync-Ends/blob/master/images/architecture.PNG" height="500" width="800"/>

## Features
|Feature|Description  |
|--|--|
|1-step execution for service |```Simple 1-step CLI execution for Sync Ends service```|
|API Change Notification  |```Get notifications about changes made to the API in Postman along with detailed diff of changes```|
|Track Postman collection | ```Ability to track a Postman collection and get notifications```|
|Slack Bot Subscription   |``` Set frequency of notifications as well as customize Slack channel for updates``` |
| | |

## Experiment Setup

### Step 1 : Setup Postman
1. Sign in to [Postman](https://identity.getpostman.com/login).
2. If you do not have any pre-exiting collections on Postman, import this sample [collection](https://www.getpostman.com/collections/dfa93d217bf211237c8f).
3. To integrate with the Sync Ends service, a Postman API key is required. Generate API key by visiting this [page](https://web.postman.co/settings/me/api-keys).
4. Copy the generated API key. This is required during the time of execution of the service. Make sure you store it safely as you won't be able to view this any other time.

### Step 2 : Create a Slack workspace and Slack bot

#### 2a.Creating Slack team
1. Open https://slack.com/.
2. Provide your email ID. Select `Create New workspace`.
3. Check your email and enter the code to verify your email.
4. Provide your name and set a password.
5. Add some details to your workspace in the next page.
6. Provide a company name.
7. Workspace URL should be unique. Also remember this URL, this is what is used to login to your Slack instance.
8. Agree with the terms.
9. Skip the invite step.
10. You are up and running with your own instance of Slack.


#### 2b. Creating Slack bot
1. Open your `<workspace-URL>/apps` (the one you created above). For example, ![https://test-visual.slack.com/apps](https://test-visual.slack.com/apps).
2. Search for bot in the search bar and select `Bots`.
3. In the Bots landing page, click on `Add configuration`.
4. Provide a Bot name. For example, `wolfpack-bot` and click on `Add Bot integration`.
5. In the `Setup instruction` page: `Copy and store the API Token`. For example, the token may look something like this: `xoxb-22672546-n1X9APk3D0tfksr81NJj6VAM`.
6. Save the Bot integration.

## Known Patterns in the code

- We are using composite and layer pattern in the code. The Parser module parse the user input and pass the parsed data to underlying layers. The sync end service accepts the data from parser layer and send the notification to slack.
- The Collection object use the composite pattern where a collection contains multiple end points and each end point has attributes like URL, method type, name, etc.

## What is Sync Ends?

Please have a look at the point descriptions of each function/class through this ![documentation file](https://github.com/jaymodi98/Sync-Ends/blob/master/docs/src/index.html) generated via `pdoc3`. To view this documentation, clone the repository and then open the linked file in the browser.

## Why use Sync Ends?
Sync ends is a state of the art technology which keeps your consumers updated with the changes to your API in realtime. Consider a user using multiple API's in thier system, In this ever changing world it is impossible for the consumer to be updated with each and every API change. Here is where sync ends comes into action. If API developers start using sync ends then the consumer will be updated in near real time with the API changes. This will make your API more robust and developers will love using such API's which provide such good support. So avoid crashes and shift to sync ends.

This version of sync ends is highly usable as it can be simply downloaded through PyPi. It is a single package which satisfies all your needs with clean documentation. Using simple config file you can start the service from terminal through our CLI interface. All your API's from postman collection will be fetched and their changes will be reflected into your slack channel.

<img src="https://github.com/jaymodi98/Sync-Ends/blob/master/src/meme.jpg" width=40% />

```Transcript(Hindi to English) - API can change anytime```

*Reference : Meme From TV Series [Mirzapur](https://www.google.com/search?q=mirzapur)*


## How to use Sync Ends?
### Installation
```
pip install sync-ends
```
The code is deployed as a python package on PyPI which is a single step installation process.

### Usage

1. The package is primarily run through a CLI (single step) for ease of use.

Run the following command with required parameters.
```
syncends  --config_file </path/to/your/local/config/file>
```
What is `--config_file`?
```
config_file - the configuration file used by application
```
How to write the config_file? (format of the file should be `.json`)
```
{
    "postman_api_key": "<a>",
    "slack_token": "<b>",
    "trigger_interval": <c>,
    "collections": [
        {
            "collection_name": "<d>",
            "slack_channel": "<e>"
        }
    ]
}
```
where,
- `a`: postman api key generated using steps shown in setup
- `b`: slack token generated using steps shown in setup
- `c`: **[optional: default=10]** time (in seconds), after which application will check for api changes
- `d`: collection name from postman collections
- `e`: **[optional: default="general"]** slack channel in which notifications will be sent (must be a public channel)

### What happens after this command is run?

This command is the entry point to a background process which fetches all the `Postman collections` using the `Postman API key` and posts a message through the `Slack bot token` configured in the `Slack channel` specified. The background service fetches the Postman collections every `trigger interval` seconds. This means that developer on changing the API in the Postman does not have to worry about notifying any API consumers of the change. That magic is done by our bot :)

## Congratulations
### **You just saved yourself from unwanted crashes**
<img src="https://media.tenor.com/images/73cca45a93f91944b2c9fdd4b05c3c53/tenor.gif"/>

## License

This project is licensed under the MIT License.
