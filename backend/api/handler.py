import json

with open("results.json") as f:
    data = json.load(f)


def handler(event, context):
    print("Event received!")
    print(event)
    return {"statusCode": 200,
            "body": json.dumps([])}
