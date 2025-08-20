import os, json, boto3

REGION = os.environ.get("AWS_REGION", "<YOUR_AWS_REGION>")
INVENTORY_TABLE = os.environ.get('INVENTORY_TABLE', '<INVENTORY_TABLE>')

dynamodb = boto3.client('dynamodb', region_name=REGION)

def _items_iter(items_any):
    if isinstance(items_any, dict):
        yield from items_any.values()
    elif isinstance(items_any, list):
        yield from items_any
    else:
        return []

def lambda_handler(event, context):
    print(f"[OrderReservation] event: {json.dumps(event)}")
    items = event["order"].get("items", {})

    try:
        transact = []
        for it in _items_iter(items):
            item_id = it["item_id"]
            qty = int(it.get("quantity", 1))
            transact.append({
                "Update": {
                    "TableName": INVENTORY_TABLE,
                    "Key": {"item_id": {"S": item_id}},
                    "UpdateExpression": "SET quantity = quantity - :q",
                    "ConditionExpression": "quantity >= :q",
                    "ExpressionAttributeValues": {":q": {"N": str(qty)}}
                }
            })
        if transact:
            dynamodb.transact_write_items(TransactItems=transact)
        return {"reserved": True}
    except dynamodb.exceptions.TransactionCanceledException as e:
        print(f"[OrderReservation] TransactionCanceled: {e}")
        raise
    except Exception as e:
        print(f"[OrderReservation] ERROR: {e}")
        raise
