import json

def unmarshall_item(d):
    """Functie helper recursiva pentru a transforma formatul DynamoDB in JSON simplu."""
    if isinstance(d, dict):
        if len(d) == 1:
            key, value = list(d.items())[0]
            if key == 'S': return str(value)
            elif key == 'N': return int(value) if '.' not in str(value) else float(value)
            elif key == 'B': return value
            elif key == 'BOOL': return bool(value)
            elif key == 'NULL': return None
            elif key == 'M': return {k_inner: unmarshall_item(v_inner) for k_inner, v_inner in value.items()}
            elif key == 'L': return [unmarshall_item(v_inner) for v_inner in value]
        return {k: unmarshall_item(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [unmarshall_item(v) for v in d]
    return d

def lambda_handler(event, context):
    """
    Acest handler primeste o LISTA de la Pipe, dar returneaza UN SINGUR OBIECT.
    """
    print(f"Received event list from Pipe: {json.dumps(event)}")
    
    # Validam ca input-ul este o lista si nu este goala
    if not isinstance(event, list) or not event:
        print("Input is not a list or is empty. Exiting.")
        return {}
        
    # --- PASUL 1: Extragem PRIMUL (si singurul) obiect din lista ---
    # Aceasta este cheia problemei. Procesam doar primul record din lot.
    record = event[0]
    
    if 'dynamodb' in record and 'NewImage' in record['dynamodb']:
        dynamodb_item = record['dynamodb']['NewImage']
        
        # Pasul 2: Transforma din format DynamoDB in JSON curat
        clean_order_object = unmarshall_item(dynamodb_item)
        
        # Pasul 3 (Optional, dar recomandat): Transforma 'items' din lista in obiect
        if 'items' in clean_order_object and isinstance(clean_order_object['items'], list):
            items_list = clean_order_object['items']
            items_map = {f"item_{i}": item for i, item in enumerate(items_list)}
            clean_order_object['items'] = items_map
            
        # Pasul 4: Impacheteaza in formatul final asteptat de State Machine
        final_payload = {'order': clean_order_object}
        
        print(f"SUCCESS: Returning a SINGLE JSON OBJECT to the State Machine: {json.dumps(final_payload)}")
        
        # --- PASUL 5 (CRUCIAL): Returneaza direct obiectul, NU o lista ---
        return final_payload
        
    print("Record structure invalid. Exiting.")
    return {}