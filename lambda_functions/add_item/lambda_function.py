import boto3
import json
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Inventory')

def lambda_handler(event, context):
    # Parse the incoming request body
    data = json.loads(event['body'])
    item_id = str(uuid.uuid4())
    data['id'] = item_id

    # Save the item to DynamoDB
    table.put_item(Item=data)

    return {
        'statusCode': 201,
        'headers': {
            'Access-Control-Allow-Origin': '*',  # Allows all origins
        },
        'body': json.dumps({'message': 'Item added successfully', 'item': data})
    }
