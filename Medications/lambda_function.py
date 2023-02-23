import boto3
import simplejson as json
import logging

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Medications')

def lambda_handler(event, context):
    print('Event payload: ' + json.dumps(int(event['pathParameters']['id'])))
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
        medications = {
            'id': int(event['pathParameters']['id']),
            'name': event['name'],
            'medication_id': event['medication_id'],
            'compound_id': event['compound_id'],
            'price': float(event['price'])
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
        id = int(event['pathParameters']['id'])
        expression_attribute_values = {}
        update_expression = 'SET'
        
        for key in event['body']:
            if key != 'id':
                if key == 'price':
                    expression_attribute_values[':{}'.format(key)] = float(event['body'][key])
                else:
                    expression_attribute_values[':{}'.format(key)] = event['body'][key]
                
                update_expression += ' #{} = :{},'.format(key, key)
                expression_attribute_values['#{}'.format(key)] = key
        
        update_expression = update_expression[:-1]
        result = table.update_item(
            Key={'id': id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues='ALL_NEW'
        )
        response = {
            'statusCode': 200,
            'body': json.dumps(result['Attributes'])
        }
    except Exception as e:
        response = {
            'statusCode': 500,
            'body': json.dumps('Error updating medication: {}'.format(str(e)))
        }
    
    return response

def delete_medication(event, context):
    try:
        id = event['pathParameters']['id']
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
