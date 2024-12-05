import boto3
import json
from decimal import Decimal

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Inventory')

# Custom JSON serializer for Decimal types
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    try:
        # Parse the request body
        data = json.loads(event['body'])
        item_id = data['id']  # Expecting the item ID in the body

        # Create the update expression dynamically
        update_expression = "SET "
        expression_attribute_names = {}
        expression_attribute_values = {}
        for key, value in data.items():
            if key != "id":  # Don't update the ID
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
            'body': json.dumps({
                'message': 'Item updated successfully',
                'updatedAttributes': response.get('Attributes', {})
            }, cls=DecimalEncoder)
        }

    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
