from uuid import uuid4
from datetime import datetime

import boto3
from boto3.dynamodb.conditions import Key

from .lambda_responses import bad_request, create_response, delete_response, get_response, internal_server_error, update_response

CONTACTS_TABLE_NAME = "Contacts"
CONTACTS = boto3.resource("dynamodb").Table(CONTACTS_TABLE_NAME)


def generate_ddb_update_expression(body):
    """Given a dictionary we generate an update expression and a dict of values
    to update a dynamodb table.

    Params:
        body (dict): Parameters to use for formatting.

    Returns:
        update expression, dict of values.
    """
    update_expression = ["set "]
    update_values = dict()

    for key, val in body.items():
        update_expression.append(f" {key} = :{key},")
        update_values[f":{key}"] = val

    return "".join(update_expression)[:-1], update_values


def add_contact(request_body):
    print("input to lambda :::::", request_body)
    user_id = request_body['user_id']
    first_name = request_body.get('first_name') or ""
    last_name = request_body.get('last_name') or ""

    item_to_insert = {
        "contact_id": str(uuid4()),
        "first_name": first_name,
        "last_name": last_name,
        "full_name": f"{first_name} {last_name}",
        "email_id": request_body.get("email_id") or "",
        "phone_number": request_body.get("phone_number") or "",
        "dial_code": request_body.get("dial_code") or "",
        "created_by": user_id,
        "created_at": str(datetime.utcnow()), 
    }
    try:
        CONTACTS.put_item(Item=item_to_insert)
        return create_response()
    except Exception as error:
        print("this is the error msg : ", error)
        return internal_server_error()


def edit_contact(request_body):
    contact_id = request_body["contact_id"]
    details_to_update = request_body.get("update_details")

    if details_to_update:
        artts, vls = generate_ddb_update_expression(details_to_update)
        response = CONTACTS.update_item(
            Key={'contact_id': contact_id},
            UpdateExpression=artts,
            ExpressionAttributeValues=dict(vls)
            )
    else:
        return bad_request("No details provided to update")

    return update_response()

def get_contacts(request_body):
    try:
        created_by = request_body["user_id"]
        list_of_contacts = CONTACTS.query(
            IndexName='created_by-index',
            KeyConditionExpression=Key("created_by").eq(created_by),
        )["Items"]
        return get_response(list_of_contacts)
    except Exception as error:
        print("error ::::", error)
        return internal_server_error()


def delete_contact(request_body):
    try:
        contact_id = request_body["contact_id"]
        CONTACTS.delete_item(Key={'contact_id': contact_id})
        return delete_response()
    except Exception as error:
        print("error ::::", error)
        return internal_server_error()