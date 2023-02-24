<!-- @format -->

# Medication Service

This is a serverless microservice for managing medication data. It uses AWS Lambda, Amazon API Gateway, and Amazon DynamoDB to provide a scalable and cost-effective solution for storing and retrieving medication data.
Getting Started

To get started, you will need an AWS account and the AWS CLI installed on your machine. Once you have these set up, you can follow the steps below to deploy the microservice:

🔧 Configuration Instructions

Create a DynamoDB table: First, you need to create a DynamoDB table to store medication data. You can do this using the AWS Management Console or the AWS CLI. Here's an example command to create a table:

```
aws dynamodb create-table --table-name Medications --attribute-definitions AttributeName=id,AttributeType=N AttributeName=name,AttributeType=S AttributeName=medication_id,AttributeType=S AttributeName=price,AttributeType=N --key-schema AttributeName=id,KeyType=HASH --billing-mode PAY_PER_REQUEST
```

Create a Lambda function: Next, you need to create a Lambda function that handles requests from the API Gateway and performs CRUD operations on the DynamoDB table. You can create the function using the AWS Management Console or the AWS CLI. Here's an example command to create a function:

```
aws lambda create-function --function-name MedicationService --runtime python3.8 --handler lambda_function.lambda_handler --zip-file fileb://path/to/your/code.zip --timeout 30 --memory-size 128 --environment Variables={TABLE_NAME=Medications}
```

Configure the API Gateway: Once you have created the Lambda function, you need to configure the API Gateway to route requests to the function. You can do this using the AWS Management Console or the AWS CLI. Here's an example command to create an API:

```
aws apigateway create-rest-api --name MedicationAPI
```

Add API resources and methods: Once you have created the API, you need to add resources and methods to it to define the API endpoints. You can do this using the AWS Management Console or the AWS CLI. Here's an example command to add a resource:

```
aws apigateway create-resource --rest-api-id YOUR_API_ID --parent-id YOUR_PARENT_RESOURCE_ID --path-part medications
```

Configure the authorizer for the API Gateway: You need to configure the API Gateway to use the Lambda authorizer function for authenticating and authorizing incoming requests. Here's an example command to add an authorizer to a method:

```
aws apigateway update-method --rest-api-id YOUR_API_ID --resource-id YOUR_RESOURCE_ID --http-method GET --authorization-type CUSTOM --authorizer-id YOUR_AUTHORIZER_FUNCTION_ARN
```

Update the method integration: After configuring the authorizer, you need to update the method integration to route requests to the Lambda function. Here's an example command to update a method integration:

```
aws apigateway put-integration --rest-api-id YOUR_API_ID --resource-id YOUR_RESOURCE_ID --http-method GET --type AWS_PROXY --integration-http-method POST --uri arn:aws:apigateway:us-west-2:lambda:path/2015-03-31/functions/YOUR_LAMBDA_FUNCTION_ARN/invocations --credentials YOUR_ROLE_ARN
```

Deploy the API: Finally, you need to deploy the API to make it accessible to clients. You can do this using the AWS Management Console or the AWS CLI. Here's an example command to deploy the API:

```
aws apigateway create-deployment --rest-api-id YOUR_API_ID --stage-name YOUR_STAGE_NAME
```

🚀 Serverless Microservices Pattern

This microservice implements the "API Gateway and Lambda" pattern, which involves using AWS Lambda to host the application logic, and Amazon API Gateway to create a RESTful API that acts as a front-end for the Lambda function. The API Gateway provides a secure, scalable, and managed entry point for clients to interact with the microservice. When a client sends an HTTP request to the API, the API Gateway routes the request to the appropriate Lambda function for processing. The Lambda function then executes the application logic and returns a response to the API Gateway, which in turn returns the response to the client.

## Usage

You can test the microservice using a tool like Postman. Here are some example API endpoints:

```
POST /medications
{
    "id": 1,
    "name": "Ibuprofen",
    "medication_id": "DB01050",
    "price": 9.98
}
```

Get a medication:

```
GET /medications/1
```

Update a medication:

```
PUT /medications/1
{
    "id": 1,
    "name": "Ibuprofen",
    "medication_id": "DB01050",
    "price": 8.99
}
```

Delete a medication:

```
DELETE /medications/1
```

Note: Replace /medications with the appropriate base URL for your deployed API.

The above endpoints correspond to the CRUD operations performed by the Lambda function in the code you provided.

To test the microservice, you can use a tool like Postman to make HTTP requests to the API Gateway. When you make a request to the API, the API Gateway will route the request to the appropriate Lambda function, which will execute the corresponding CRUD operation on the DynamoDB table.

To add the authorizationToken header to your requests in Postman, you can follow these steps:

    Open Postman and navigate to the request you want to add the header to.

    Click on the "Headers" tab below the request URL field.

    Click on the "Add Header" button.

    Enter "authorizationToken" as the header key.

    Enter "xxxxxxxxxx" as the header value. [Modify this value in the lambda function]

    Leave the "description" field blank.

    Set the "type" field to "text".

    Make sure the "enabled" checkbox is checked.

    Click the "Save" button to save the header.

Once you've added the header to your request, you should be able to successfully authenticate with the Lambda authorizer function.

## Conclusion

That's it! You now have a fully functional serverless microservice for managing medication data. With this architecture, you can easily scale your application as your user base grows, without having to worry about managing and scaling the underlying infrastructure.
