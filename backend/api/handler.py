import json


with open("data/results.json") as f:
    data = json.load(f)

with open("data/imagenet_class_index.json") as f:
    imagenet_class_index = json.load(f)


def format_response(message, data):
    return {
        "message": message,
        "data": data
    }


def handler(event, context):
    print("Event received!")
    print(event)
    response = []
    if event['queryStringParameters']:
        print(event['queryStringParameters'])
        query = event['queryStringParameters']["q"]
        search_type = event['queryStringParameters']["search"]
        if search_type == "classes":
            if query in imagenet_class_index.keys():
                print(imagenet_class_index[query])
                print(type(imagenet_class_index[query]))
                response = format_response(message="", data=data[str(imagenet_class_index[query])]["images"])
        elif search_type == "tags":
            response = format_response(message="TAG SEARCH", data=[])

    return {"statusCode": 200,
            "headers": {
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Origin": "https://master.d2qdeae4ccxv4a.amplifyapp.com",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                "Content-Type": "application/json"
            },
            "body": json.dumps(response)}
