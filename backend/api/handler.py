import json

with open("results.json") as f:
    data = json.load(f)


def handler(event, context):
    print("Event received!")
    print(event)
    if event['queryStringParameters']:
        print(event['queryStringParameters'])
    return {"statusCode": 200,
            "headers": {
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Origin": "https://master.d2qdeae4ccxv4a.amplifyapp.com",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                "Content-Type": "application/json"
            },
            "body": json.dumps(data["1"]["images"])}
