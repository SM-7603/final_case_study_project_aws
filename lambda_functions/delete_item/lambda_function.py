import boto3
import json

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Inventory')

def lambda_handler(event, context):
    try:
        # Extract the 'id' from the pathParameters
        item_id = event['pathParameters']['id']

        # Delete the item in DynamoDB
        table.delete_item(Key={'id': item_id})

        return {
            'statusCode': 200,
            'body': json.dumps({'message': f'Item with id {item_id} deleted successfully'})
        }

    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
