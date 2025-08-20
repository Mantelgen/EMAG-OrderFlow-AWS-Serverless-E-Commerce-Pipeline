import os, json, boto3

REGION = os.environ.get("AWS_REGION", "<YOUR_AWS_REGION>")
ORDERS_TABLE = os.environ.get('ORDERS_TABLE', '<ORDERS_TABLE>')
INVENTORY_TABLE = os.environ.get('INVENTORY_TABLE', '<INVENTORY_TABLE>')
CUSTOMERS_TABLE = os.environ.get('CUSTOMERS_TABLE', '<CUSTOMERS_TABLE>')

dynamodb = boto3.resource('dynamodb', region_name=REGION)
customers_table = dynamodb.Table(CUSTOMERS_TABLE)
inventory_table = dynamodb.Table(INVENTORY_TABLE)

def _bad(msg): return {"isValid": False, "message": msg}

def _items_iter(items_any):
    # acceptă map (dict) sau listă
    if isinstance(items_any, dict):
        yield from items_any.values()
    elif isinstance(items_any, list):
        yield from items_any
    else:
        raise ValueError("order.items trebuie să fie dict sau list")

def lambda_handler(event, context):
    print(f"[ValidateOrder] event: {json.dumps(event)}")
    try:
        order = event["order"]
        customer_id = order["customer_id"]
        items = order.get("items")
        if not items:
            return _bad("Order has no items")

        # client valid?
        cust = customers_table.get_item(Key={"customer_id": customer_id}).get("Item")
        if not cust:
            return _bad(f"Customer {customer_id} not found")

        # produse + stoc
        for it in _items_iter(items):
            item_id = it["item_id"]
            qty = int(it.get("quantity", 1))
            inv = inventory_table.get_item(Key={"item_id": item_id}).get("Item")
            if not inv:
                return _bad(f"Item {item_id} not found")
            if int(inv.get("quantity", 0)) < qty:
                return _bad(f"Insufficient stock for {item_id} (need {qty})")

        return {"isValid": True}
    except KeyError as e:
        return _bad(f"Missing required field: {e}")
    except Exception as e:
        print(f"[ValidateOrder] ERROR: {e}")
        return _bad("Internal validation error")
