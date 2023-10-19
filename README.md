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

## Table of Contents
  * [Architecture Diagram](#architecture-diagram)
  * [Features](#features)
  * [Patterns in the code](#patterns-in-the-code)
  * [Documentation](#documentation)
    + [What is Sync Ends?](#what-is-sync-ends)
    + [Why use Sync Ends?](#why-use-sync-ends)
    + [How to use Sync Ends?](#how-to-use-sync-ends)
      - [Installation](#installation)
      - [Usage](#usage)
        * [How to write the config_file? (format of the file should be `.json`)](#how-to-write-the-config_file-format-of-the-file-should-be-json)
      - [What happens after this command is run?](#what-happens-after-this-command-is-run)
    + [Setup Postman and Teams channels](#setup-postman-and-teams-channels)
      - [Step 1 : Setup Postman](#step-1--setup-postman)
      - [Step 2 : Create a Slack workspace and integrate Slack bot](#step-2--create-a-slack-workspace-and-integrate-slack-bot)
        * [2a. Creating Slack workspace](#2a-creating-slack-workspace)
        * [2b. Creating Slack bot](#2b-creating-slack-bot)
      - [Step 2 Alternative : Create a Microsoft Team and create a webhook for it](#step-2-alternate--create-a-microsoft-team-and-create-a-webhook-for-it)
        * [2a. Creating Microsoft Team](#2a-creating-microsoft-team)
        * [2b. Creating Webhook](#2b-creating-webhook)
    + [Actions reported by the Sync-Ends program](#actions-reported-by-the-sync-ends-program)
  * [How to Contribute?](#how-to-contribute)
  * [License](#license)

## Architecture Diagram
<img src="https://github.com/jaymodi98/Sync-Ends/blob/master/images/architecture.PNG" height="500" width="800"/>

## Features
|Feature|Description  |
|--|--|
|1-step service execution |```Simple 1-step CLI execution for Sync Ends service```|
|API Change Notification  |```Get notifications about changes made to the API in Postman along with detailed diff of changes```|
|Track Postman collection | ```Ability to track a Postman collection and get notifications```|
|Slack Bot Subscription   |``` Set frequency of notifications as well as customize Slack channel for updates``` |

## Patterns in the code

- We are using Composite and Layer pattern in the code. The Parser module parses the user input and passes the parsed data to the underlying layers. The `sync end service` accepts the data from the parser layer and sends the notification to Slack.
- The Collection object uses the Composite pattern where a Collection contains multiple EndPoints and each End Point has attributes such as URL, method type, name, etc.

## Documentation
### What is Sync Ends?

Please have a look at the point descriptions of each function/class through this [documentation file](https://github.com/jaymodi98/Sync-Ends/blob/master/docs/src/index.html) generated via `pdoc3`. To view this documentation, clone the repository and then open the linked file in the browser.

### Why use Sync Ends?
Sync ends is a productivity service that focuses on saving developer time by automating API changes to their consumers in real-time thus improving your team's productivity. 
Consider an API consumer using multiple APIs in their system. In this ever-changing world, it is impossible for the consumer to be updated with each and every API change. This is the problem that Sync Ends service addresses. The service is easy to install and this reduces the communication overhead on side of the API devs. So avoid crashes and jump on the Sync Ends bandwagon! :)

This version of sync ends is highly usable as it can be simply downloaded through PyPI. It is a single package which satisfies all your needs with clean documentation. Using  just a simple config file, you can start the service from terminal through our CLI interface. All your API's from the Postman collection will be fetched and their changes will be reflected as notifications in your slack channel.

<img src="https://github.com/jaymodi98/Sync-Ends/blob/master/src/meme.jpg" width=40% />

```Transcript(Hindi to English) - API can change anytime```

*Reference : Meme From TV Series [Mirzapur](https://www.google.com/search?q=mirzapur)*


### How to use Sync Ends?
#### Installation
```
pip install sync-ends
```
The code is deployed as a [python package on PyPI](https://pypi.org/project/sync-ends/) which is a single step installation process.

#### Usage

1. The package is primarily run through a CLI (single step) for ease of use.

Run the following command with required parameters.
```
python3 <path/to/main.py>  --config </path/to/your/local/config/file>
```
What is `--config`?
```
config - specifies the configuration file used by the Sync Ends service
```
##### How to write the config_file? (format of the file should be `.json`)
```
{
    "postman_api_key": "<a>",
    "slack_token": "<b>",
    "trigger_interval": <c>,
    "collections": [
        {
            "collection_name": "<d>",
            "slack_channel": "<e>",
            "microsoft_teams_webhook" : "<f>",
            "channel_type": "<g>",
            "sender_email": "<h>",
            "sender_pwd": "<i>",
            "recipient_email": "<j>"
        }
    ]
}
```
where,
- `a`: postman api key generated using steps shown in [postman setup section](#step-1--setup-postman)
- `b`: slack token generated using steps shown in [slack setup section](#step-2--create-a-slack-workspace-and-integrate-slack-bot)
- `c`: time (in seconds), after which application will periodically check for api changes
- `d`: collection name from postman collections
- `e`: slack channel in which notifications will be sent (must be a public channel)
- `f`: Microsoft teams channel webhook url [Teams setup section](#step-2-alternate--create-a-microsoft-team-and-create-a-webhook-for-it)
- `g`: string specifying which channel to send notifications to. (`slack`, `teams`, `email`, `slack_and_teams`, `slack_and_email`, `teams_and_email`, `all`)
- `h`: email address to send email notification from
- `i`: the app password generated for the senders gmail account
- `j`: email address to send email notifications

In the case where you only wish to send notifications to a slack channel or teams chat the fields for the other type can be left as empty quotes.

Example for only slack:
    "microsoft_teams_webhook" : " "
would be put into the config file and the channel_type would be set to slack


#### What happens after this command is run?

This command is the entry point to a background process which fetches all the `Postman collections` using the `Postman API key` and posts a message through the `Slack bot token` configured in the `Slack channel` specified or to the `Webhook URL` for a teams chat. The background service fetches the Postman collections every `trigger interval` seconds. Since all of this happens **automatically** after running the CLI command, this means that developer on changing the API in the Postman does not have to worry about notifying any API consumers of the change. That magic is done by our bot :)

### Setup Postman and Teams channels
#### Step 1 : Setup Postman
1. Sign in to [Postman](https://identity.getpostman.com/login). You can use your existing postman account but since you will need to share API key and login credentials with the API Developer, *we suggest creating a new account*.
2. If you do not have any pre-exiting collections on Postman, create a sample/template collection or create a new blank API collection and add APIs to it.
3. To integrate with the Sync Ends service, a Postman API key is required. Generate API key by visiting this [page](https://web.postman.co/settings/me/api-keys).
4. Copy the generated API key. This is required during the time of execution of the service. Make sure you store it safely as you won't be able to view this any other time.

#### Step 2 : Create a Slack workspace and integrate Slack bot

##### 2a. Creating Slack workspace
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

##### 2b. Creating Slack bot
1. Open your `<workspace-URL>/apps` (the one you created above). For example, [https://test-visual.slack.com/apps](https://test-visual.slack.com/apps).
2. Search for bot in the search bar and select `Bots`.
3. In the Bots landing page, click on `Add configuration`.
4. Provide a Bot name. For example, `wolfpack-bot` and click on `Add Bot integration`.
5. In the `Setup instruction` page: `Copy and store the API Token`. For example, the token may look something like this: `xoxb-22672546-n1X9APk3D0tfksr81NJj6VAM`.
6. Save the Bot integration.

#### Step 2 alternate : Create a Microsoft Team and create a webhook for it

##### 2a. Creating Microsoft Team
1. Open https://teams.microsoft.com/.
2. Sign into your Microsoft Account
3. Create a new team to get API notifications at
4. Invite people who need to see those notifications to the Team
5. You have a working Microsoft Team

##### 2b. Creating webhook
1. Enter the Microsoft Team
2. Click on the three dots to the right of the channel that you wish to have API notifications sent to
3. Select Connectors
4. Search for Incoming Webhook and click add
5. Click configure on Incoming Webhook provide a name and click create
6. Coppy the URL provided and paste it into the webhook field in the confguration JSON file

### Actions reported by the Sync-Ends program

* Adding a new API request to the collection
* Deleting a API from the collection
* Updating the name of an API
* Updating the URL of an API
* Updating the API method (GET, POST, etc.) of an API
* Updating the authentication method in the API
* Performing these steps quickly and in succession 

## Congratulations
### **You just saved yourself from unwanted crashes**
<img src="https://media.tenor.com/images/73cca45a93f91944b2c9fdd4b05c3c53/tenor.gif"/>

## How to Contribute?
Please take a look at our [CONTRIBUTING.md](https://github.com/jaymodi98/Sync-Ends/blob/master/CONTRIBUTING.md) where we provide instructions on contributing to the repo and help us in enhancing the product.

## License

This project is licensed under the MIT License.
