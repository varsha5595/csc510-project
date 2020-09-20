import http.client
from jsondiff import diff
import json
import os
import mimetypes
import re
import time
import slack
from slack import WebClient
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def get_postman_collections(connection):
    boundary = ''
    payload = ''
    headers = {
        'X-Api-Key': '',
        'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
    }
    connection.request("GET", "/collections", payload, headers)
    res = connection.getresponse()
    data = res.read()

    
def regex(value):
    regexes = ["(?<='key': )[^,||}]*", "(?<='value': )[^,||}]*", "(?<=delete: \[)[^]]+", "(?<=insert: \[)[^]]+"]
    return [re.findall(regex, value) for regex in regexes]


def get_selected_collection(collection_id, connection):
    boundary = ''
    payload = ''
    headers = {
        'X-Api-Key': '',
        'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
    }
    connection.request("GET", "/collections/" + collection_id, payload, headers)
    res = connection.getresponse()
    data = json.loads(res.read())

    with open("../data/collections/" + collection_id + ".txt", "r+") as f:
        old_value = diff(data, json.load(f))
        print(old_value)
        f.close()

    with open("../data/collections/" + collection_id + ".txt", "r+") as f:
        new_value = diff(json.load(f), data)
        print(new_value)
        f.close()

    with open("../data/collections/" + collection_id + ".txt", "w+") as f:
        json.dump(data, f)
        f.close()

    changes = [regex(str(value)) for value in [old_value, new_value]]
    keys_old = "Keys in old call: " + ' '.join(changes[0][0])
    keys_new = "Keys in new call: " + ' '.join(changes[1][0])
    ins = "pairs inserted in new call: " + ' '.join(changes[1][3])
    dels = "Row deleted from old call: " + ' '.join(changes[0][2])
    
    return keys_old + "\n" + keys_new + "\n" + ins + "\n" + dels


def main():
    postman_connection = http.client.HTTPSConnection("api.getpostman.com")
    get_postman_collections(postman_connection)
    colls = get_selected_collection("", postman_connection)
    
    # Create a slack client
    slack_web_client = WebClient(token = "")

    # Slack Channel to post the message
    channel = "postman"

    # Get the onboarding message payload
    message = {
                "channel": channel,
                "blocks": [
                    { "type": "section", "text": { "type": "plain_text", "text": colls}}
                ],
            }

    # Post the onboarding message in Slack
    slack_web_client.chat_postMessage(**message)

    
if __name__ == '__main__':
    while True:
        main()
        time.sleep(3600)

    


