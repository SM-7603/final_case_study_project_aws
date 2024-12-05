import boto3
import json
from decimal import Decimal

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Inventory')

# Custom JSON encoder for Decimal types
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)  # Convert Decimal to float
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    try:
        # Extract the 'id' from pathParameters
        item_id = event['pathParameters']['id']

        # Parse the request body
        body = json.loads(event['body'])

        # Dynamically create the update expression
        update_expression = "SET "
        expression_attribute_names = {}
        expression_attribute_values = {}
        for key, value in body.items():
            update_expression += f"#attr_{key} = :val_{key}, "
            expression_attribute_names[f"#attr_{key}"] = key
            expression_attribute_values[f":val_{key}"] = value

        update_expression = update_expression.rstrip(", ")  # Remove trailing comma

        # Update the item in DynamoDB
        response = table.update_item(
            Key={'id': item_id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Allows all origins
            },
            'body': json.dumps({
                'message': 'Item updated successfully',
                'updatedAttributes': response.get('Attributes', {})
            }, cls=DecimalEncoder)  # Use the custom encoder
        }

    except Exception as e:
        print("Error:", str(e))  # Log the error for debugging
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
