import json

def lambda_handler(event, context):
    print(f"[Shipping] event: {json.dumps(event)}")
    order = event["order"]
    addr = order.get("shipping_address", {})
    country = addr.get("country", "RO")

    base = 15.0
    intl = 20.0 if country != "RO" else 0.0

    return {"shipping_cost": base + intl, "currency": order.get("currency", "RON")}
