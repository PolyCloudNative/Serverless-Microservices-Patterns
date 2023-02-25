import simplejson as json

def lambda_handler(event, context):
    print('----- START ------')
    print(event)
    # 1. Iterate over each record
    try:
        for record in event['Records']:
            # 2. Handle event by type
            if record['eventName'] == 'INSERT':
                handle_insert(record)
            elif record['eventName'] == 'MODIFY':
                handle_modify(record)
            elif record['eventName'] == 'REMOVE':
                handle_remove(record)
        print('------------------------')
        return "Success!"
    except Exception as e:
        print(e)
        print('------------------------')
        return "Error"

def handle_modify(record):
    print("Handling MODIFY Event")

    # 3a. Parse oldImage and price
    oldImage = record['dynamodb']['OldImage']
    oldPrice = oldImage['price']['N'] if 'price' in oldImage else None

    # 3b. Parse newImage and price
    newImage = record['dynamodb']['NewImage']
    newPrice = newImage['price']['N'] if 'price' in newImage else None

    # 3c. Check for change
    if oldPrice is not None and newPrice is not None and oldPrice != newPrice:
        print('Price changed - oldPrice=' + str(oldPrice) + ', newPrice=' + str(newPrice))

    print("Done handling MODIFY Event")