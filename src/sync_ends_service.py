import http.client
import jsondiff
from jsondiff import diff
import json
import os
import mimetypes
import re
import time
import slack
from slack import WebClient
import ssl
import sys

ssl._create_default_https_context = ssl._create_unverified_context

def get_postman_collections(connection, api_key):
    boundary = ''
    payload = ''
    headers = {
        'X-Api-Key': api_key,
        'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
    }
    connection.request("GET", "/collections", payload, headers)
    response = connection.getresponse()
    if response.status == 200:
        return response
    else:
        raise Exception("Exited with status code " + str(response.status) + '. '+ str(json.loads(response.read())['error']['message']))


def regex(value):
    regexes = ["(?<='key': )[^,||}]*", "(?<='value': )[^,||}]*", "(?<=delete: \[)[^]]+", "(?<=insert: \[)[^]]+"]
    return [re.findall(regex, value) for regex in regexes]


def get_selected_collection(collection_id, connection, api_key):
    boundary = ''
    payload = ''
    headers = {
        'X-Api-Key': api_key,
        'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
    }
    connection.request("GET", "/collections/" + collection_id, payload, headers)
    response = connection.getresponse()
    if response.status == 200:
        data = json.loads(response.read())

        filepath = "./data/" + collection_id + ".txt"
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        if not os.path.exists(filepath):
            with open(filepath, "w") as f:
                f.write("{}")
                f.close()
        
        with open(filepath, "r+") as f:
            old_value = diff(data, json.load(f))
            f.close()

        with open(filepath, "r+") as f:
            new_value = diff(json.load(f), data)
            f.close()

        changes = [regex(str(value)) for value in [old_value, new_value]]

        if changes:
            with open(filepath, "w+") as f:
                json.dump(data, f)
                f.close()
        
        keys_old = "Keys in old call: " + ' '.join(changes[0][0])
        keys_new = "Keys in new call: " + ' '.join(changes[1][0])
        ins = "Pairs inserted in new call: " + ' '.join(changes[1][3])
        dels = "Row deleted from old call: " + ' '.join(changes[0][2])
        
        return keys_old + "\n" + keys_new + "\n" + ins + "\n" + dels
    else:
        raise Exception("Exited with status code " + str(response.status) + '. '+ str(json.loads(response.read())['error']['message']))


def main():
    try:
        postman_connection = http.client.HTTPSConnection("api.getpostman.com")

        print("\nWelcome to Sync Ends! End your development overheads today!")
        print("-----------------------------------------------------------")
        print("\nLet's begin by linking your Postman account with our service!")
        api_key = input("Enter the API key for you Postman account: ")

        collections_response = get_postman_collections(postman_connection, api_key)
        all_collections = json.loads(collections_response.read())
        
        print("\nChoose a collection you would like to integrate:")

        for index, collection in enumerate(all_collections['collections'], 1):
            print(str(index) + '. ' + str(collection['name'])) 

        collection_choice = input("\nEnter your choice: ")
        selected_collection = all_collections['collections'][int(collection_choice) - 1]

        print("\nAlmost there, let's link the Slack bot to our service!")
        slack_token = input("Enter the API token for the Slack bot: ")
        
        while True:
            changes_detected = get_selected_collection(selected_collection['uid'], postman_connection, api_key)
            
            # Create a slack client
            slack_web_client = WebClient(token = slack_token)

            # Slack Channel to post the message
            channel = "postman"

            # Get the onboarding message payload
            message = {
                        "channel": channel,
                        "blocks": [
                            { "type": "section", "text": { "type": "plain_text", "text": changes_detected}}
                        ],
                    }

            # Post the onboarding message in Slack
            slack_web_client.chat_postMessage(**message)
            time.sleep(3600)
    except Exception as e:
        print(e)

    
if __name__ == '__main__':
    main()
