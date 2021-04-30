import re
import json
import pickle

import numpy


with open("data/results.p", "rb") as f:
    data = pickle.load(f)

with open("data/imagenet_class_index.p", "rb") as f:
    imagenet_class_index = pickle.load(f)


def format_response(message, images):
    return {
        "message": message,
        "images": images
    }


def preprocess_text(text):
    text = re.sub("[-$%@#/?!.,()0-9]", "", text).lower()
    return text.replace("  ", " ")


def handler(event, context):
    print("Event received!")
    print(event)
    response = format_response("No results", [])
    if event['queryStringParameters']:
        print(event['queryStringParameters'])
        query = event['queryStringParameters']["q"]
        search_type = event['queryStringParameters']["search"]
        query = preprocess_text(query)
        if search_type == "classes":
            if query in imagenet_class_index.keys():
                print(imagenet_class_index[query])
                print(type(imagenet_class_index[query]))
                response = format_response(message="", images=data[str(imagenet_class_index[query])]["images"])
            else:
                response = format_response(
                    f"No matches for class {event['queryStringParameters']['q']} in class index!", [])
        elif search_type == "tags":
            with open("data/inverted_tag_index_loaded_postings_v2.p", "rb") as fl:
                tags = pickle.load(fl)
            if query in tags:
                response = format_response(message="TAG SEARCH", images=tags[query])
            else:
                response = format_response(
                    f"No matches for class {event['queryStringParameters']['q']} in tags index!", [])

    return {"statusCode": 200,
            "headers": {
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Origin": "https://master.d2qdeae4ccxv4a.amplifyapp.com",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                "Content-Type": "application/json"
            },
            "body": json.dumps(response)}
