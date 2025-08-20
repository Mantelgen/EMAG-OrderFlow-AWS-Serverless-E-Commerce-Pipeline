import os, json, boto3
from botocore.exceptions import ClientError
from decimal import Decimal

REGION = os.environ.get("AWS_REGION", "<YOUR_AWS_REGION>")
ORDERS_TABLE = os.environ.get('ORDERS_TABLE', '<ORDERS_TABLE>')
dynamodb = boto3.resource('dynamodb', region_name=REGION)
orders_table = dynamodb.Table(ORDERS_TABLE)

def _to_decimal(obj):
    """Converteste recursiv float -> Decimal (safe pt DynamoDB)."""
    if isinstance(obj, float):
        # folosim str() ca sa evitam probleme de binaritate
        return Decimal(str(obj))
    if isinstance(obj, list):
        return [_to_decimal(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _to_decimal(v) for k, v in obj.items()}
    return obj

def lambda_handler(event, context):
    # event: { "order_id": "...", "status": "PAID"|"PAYMENT_FAILED", "paymentResult": {...} }
    print(f"[UpdateOrderStatus] event: {json.dumps(event)}")
    order_id = event["order_id"]
    status = event["status"]
    payment_raw = event.get("paymentResult", {})

    # === PATCH CRUCIAL: convertim float -> Decimal in ce scriem in DynamoDB ===
    payment = _to_decimal(payment_raw)

    try:
        orders_table.update_item(
            Key={"order_id": order_id},
            UpdateExpression="SET #s = :s, payment_info = :p",
            ExpressionAttributeNames={"#s": "status"},
            ExpressionAttributeValues={
                ":s": status,
                ":p": payment
            },
            ConditionExpression="attribute_exists(order_id)"
        )
        return {"updated": True}
    except ClientError as e:
        print(f"[UpdateOrderStatus] ERROR: {e}")
        raise
