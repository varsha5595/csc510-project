# Standard library imports
import http.client
import json
import os
import mimetypes
import re
import time
import ssl
import sys

# Third party imports
import jsondiff
from jsondiff import diff
import slack
from slack import WebClient

ssl._create_default_https_context = ssl._create_unverified_context


def get_postman_collections(connection, api_key):
    '''
    Input: Postman connection object, Postman API key of the user
    Description: To fetch all the collections present in the user's Postman account
    Returns all the collections in the user's Postman account
    '''
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
    '''
    TODO 
    '''
    change_detection_regex = ["(?<='key': )[^,||}]*", "(?<='value': )[^,||}]*", "(?<=delete: \[)[^]]+", "(?<=insert: \[)[^]]+"]
    return [re.findall(regex, value) for regex in change_detection_regex]


def get_selected_collection(collection_id, connection, api_key):
    '''
    Input: Postman connection object, UUID of the collection chosen by the user, Postman API key of the user
    Description: To fetch details about all the APIs present in a specfic collection and to detect changes if any
    Returns the changes detected in the API schema
    '''
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

        # For each collection, a separate text file is created to store the details related to the collection
        filepath = "./data/" + collection_id + ".txt"
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        if not os.path.exists(filepath):
            with open(filepath, "w") as f:
                f.write("{}")
                f.close()
        
        # Difference between the data received as part of the current API call and the data that previously existed in the .txt file
        # The difference is computed twice to detect changes w.r.t to addition as well as deletion of key value pairs
        with open(filepath, "r+") as f:
            old_value = diff(data, json.load(f))
            f.close()

        with open(filepath, "r+") as f:
            new_value = diff(json.load(f), data)
            f.close()

        # TODO
        changes_detected = [regex(str(value)) for value in [old_value, new_value]]

        # When changes are detected, the .txt file is updated according to the new API schema
        if changes_detected:
            with open(filepath, "w+") as f:
                json.dump(data, f)
                f.close()
        
        # Formatting the changes detected to make it user-friendly
        keys_old = "Old name of the query paramter: " + ' '.join(changes_detected[0][0])
        keys_new = "Updated name of the query parameter: " + ' '.join(changes_detected[1][0])
        keys_inserted = "Name of the query parameter newly added: " + ' '.join(changes_detected[1][3])
        keys_deleted = "Name of the query paramter that is deleted " + ' '.join(changes_detected[0][2])

        return keys_old + "\n" + keys_new + "\n" + keys_inserted + "\n" + keys_deleted
    else:
        raise Exception("Exited with status code " + str(response.status) + '. '+ str(json.loads(response.read())['error']['message']))


def main():
    try:
        postman_connection = http.client.HTTPSConnection("api.getpostman.com")

        print("\nWelcome to Sync Ends! End your development overheads today!")
        print("-----------------------------------------------------------")

        # The Postman API key is required to access all the postman collections in a user's account
        print("\nLet's begin by linking your Postman account with our service!")
        api_key = input("Enter the API key for you Postman account: ")

        # To get the collections present in a user's Postman account
        collections_response = get_postman_collections(postman_connection, api_key)
        all_collections = json.loads(collections_response.read())
        
        while True:
            print("\nChoose a collection you would like to integrate:")

            # User selects a specfic collection to be linked to the sync ends service
            for index, collection in enumerate(all_collections['collections'], 1):
                print(str(index) + '. ' + str(collection['name']))
            collection_choice = input("\nEnter your choice: ")

            if 1 <= int(collection_choice) <= len(all_collections['collections']):
                break
        
        selected_collection = all_collections['collections'][int(collection_choice) - 1]

        print("\nAlmost there, let's link the Slack bot to our service!")
        slack_token = input("Enter the API token for the Slack bot: ")
        
        while True:
            # TODO
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
