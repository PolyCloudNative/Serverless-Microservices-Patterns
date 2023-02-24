import boto3
import simplejson as json
import logging
from decimal import Decimal


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Medications')

def lambda_handler(event, context):
    http_method = event['httpMethod']
    try:
        http_method = event['httpMethod']
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps('Missing HTTP method')
        }
    
    if http_method == 'POST':
        response = create_medication(event, context)
    elif http_method == 'GET':
        response = get_medication(event, context)
    elif http_method == 'PUT':
        response = update_medication(event, context)
    elif http_method == 'DELETE':
        response = delete_medication(event, context)
    else:
        response = {
            'statusCode': 405,
            'body': json.dumps('HTTP method not supported')
        }
    
    return response

def create_medication(event, context):
    try:
        body = json.loads(event['body'])
        id = body.get('id')
        name = body.get('name')
        medication_id = body.get('medication_id')
        price = Decimal(str(body.get('price')))

        if id is None or name is None or medication_id is None:
            return {
                'statusCode': 400,
                'body': json.dumps('Missing required fields')
            }

        medications = {
            'id': id,
            'name': name,
            'medication_id': medication_id,
            'price': price
        }
        table.put_item(Item=medications)
        response = {
            'statusCode': 200,
            'body': json.dumps('Medication created successfully')
        }
    except Exception as e:
        response = {
            'statusCode': 500,
            'body': json.dumps('Error creating medication: {}'.format(str(e)))
        }
    
    return response


def get_medication(event, context):
    try:
        id = int(event['pathParameters']['id'])
        print('Retrieving medication with ID {}'.format(id))
        logging.info('Retrieving medication with ID {}'.format(id))
        result = table.get_item(Key={'id': id})
        print('Result: {}'.format(result))
        print('Event result: ' + json.dumps(result))
        medications = result.get('Item')
        if not medications:
            response = {
                'statusCode': 404,
                'body': json.dumps('Medication not found')
            }
        else:
            response = {
                'statusCode': 200,
                'body': json.dumps(medications)
            }
    except Exception as e:
        response = {
            'statusCode': 500,
            'body': json.dumps('Error getting medication: {}'.format(str(e)))
        }
    
    return response


def update_medication(event, context):
    try:
        body = {
            "id": 2,
            "medication_id": "DB01050",
            "name": "Ibuprofen",
            "price": 9.98
        }
        id = body.get('id')
        name = body.get('name')
        medication_id = body.get('medication_id')
        price = Decimal(str(body.get('price')))

        if id is None or name is None or medication_id is None:
            return {
                'statusCode': 400,
                'body': json.dumps('Missing required fields')
            }

        medications = {
            'id': id,
            'name': name,
            'medication_id': medication_id,
            'price': price
        }
        table.update_item(
            Key={'id': id},
            UpdateExpression='SET #n = :val1, medication_id = :val2, price = :val3',
            ExpressionAttributeNames={'#n': 'name'},
            ExpressionAttributeValues={
                ':val1': name,
                ':val2': medication_id,
                ':val3': price
            }
        )
        response = {
            'statusCode': 200,
            'body': json.dumps('Medication updated successfully')
        }
    except Exception as e:
        response = {
            'statusCode': 500,
            'body': json.dumps('Error updating medication: {}'.format(str(e)))
        }

    return response


def delete_medication(event, context):
    try:
        id = int(event['pathParameters']['id'])
        table.delete_item(Key={'id': id})
        response = {
            'statusCode': 200,
            'body': json.dumps('Medication deleted successfully')
        }
    except Exception as e:
        response = {
            'statusCode': 500,
            'body': json.dumps('Error deleting medication: {}'.format(str(e)))
        }
    
    return response
