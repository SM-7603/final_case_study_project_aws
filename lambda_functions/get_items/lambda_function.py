import boto3
import json
from decimal import Decimal

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Inventory')

# Custom JSON serializer for DynamoDB's Decimal type
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)  # Convert Decimal to float
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    # Scan the table to get all items
    response = table.scan()
    items = response.get('Items', [])
    
    # Return the items as JSON, using the custom DecimalEncoder
    return {
        'statusCode': 200,
        'body': json.dumps({'items': items}, cls=DecimalEncoder)
    }
