import os, json, boto3

REGION = os.environ.get("AWS_REGION", "<YOUR_AWS_REGION>")
FROM_EMAIL = os.environ.get('FROM_EMAIL', '<YOUR_EMAIL>')
CUSTOMERS_TABLE = os.environ.get('CUSTOMERS_TABLE', '<CUSTOMERS_TABLE>')

ses = boto3.client('ses', region_name=REGION)
dynamodb = boto3.resource('dynamodb', region_name=REGION)
customers_table = dynamodb.Table(CUSTOMERS_TABLE)

def _get_email_from_event_or_db(event):
    order = event.get("order", {})
    if order.get("customer_email"):
        return order["customer_email"]
    cust_id = order.get("customer_id")
    if cust_id:
        item = customers_table.get_item(Key={"customer_id": cust_id}).get("Item")
        if item and item.get("email"):
            return item["email"]
    return None

def lambda_handler(event, context):
    print(f"[SendFailMail] event: {json.dumps(event)}")
    email = _get_email_from_event_or_db(event) or "<CUSTOMER_EMAIL>"

    order = event["order"]
    subject = f"Plata pentru comanda {order['order_id']} nu a reușit"
    body = (
        f"Bună,\n\nPlata pentru comanda {order['order_id']} nu a putut fi procesată.\n"
        f"Te rugăm să reîncerci.\n"
    )

    ses.send_email(
        Source=FROM_EMAIL,
        Destination={"ToAddresses": [email]},
        Message={
            "Subject": {"Data": subject, "Charset": "UTF-8"},
            "Body": {"Text": {"Data": body, "Charset": "UTF-8"}}
        }
    )
    return {"emailSent": True}
