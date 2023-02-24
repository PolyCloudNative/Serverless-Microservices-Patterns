def lambda_handler(event, context):
    # Extract the token from the request
    print(event)
    token = event['authorizationToken']
    print(token)

    # Check if the token is valid
    if token == 'PUT_SOME_KEY':
        # If the token is valid, return an Allow policy
        return {
            'principalId': 'user',
            'policyDocument': {
                'Version': '2012-10-17',
                'Statement': [
                    {
                        'Action': 'execute-api:Invoke',
                        'Effect': 'Allow',
                        'Resource': 'arn:aws:execute-api:us-west-2:YOUR_ACCOUNT_NUM:87a3ea7lg7/*/*'
                    }
                ]
            }
        }
    else:
        # If the token is not valid, return a Deny policy
        return {
            'principalId': 'user',
            'policyDocument': {
                'Version': '2012-10-17',
                'Statement': [
                    {
                        'Action': 'execute-api:Invoke',
                        'Effect': 'Deny',
                        'Resource': 'arn:aws:execute-api:us-west-2:YOUR_ACCOUNT_NUM:87a3ea7lg7/*/*'
                    }
                ]
            }
        }
