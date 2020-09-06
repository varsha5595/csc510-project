import http.client
from jsondiff import diff
import json
import os
import mimetypes


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


def main():
    postman_connection = http.client.HTTPSConnection("api.getpostman.com")
    get_postman_collections(postman_connection)
    get_selected_collection("", postman_connection)


if __name__ == '__main__':
    main()
