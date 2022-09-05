from contacts_api import add_contact, edit_contact, delete_contact, get_contacts
from lambda_responses import bad_request


def lambda_handler(event, context):
    
    if "action" in event.keys():
        action = event['action']
    else:
        return bad_request()

    if action == 'create':
        return add_contact(event)
    elif action == 'update':
        return edit_contact(event)
    elif action == 'get':
        return get_contacts(event)
    elif action == 'delete':
        return delete_contact(event)



'''
POST - https://rm9l6gpxpi.execute-api.us-east-1.amazonaws.com/dev/user/contacts
GET - https://rm9l6gpxpi.execute-api.us-east-1.amazonaws.com/dev/user/contacts/{contact_id}
PUT - https://rm9l6gpxpi.execute-api.us-east-1.amazonaws.com/dev/user/contacts/{contact_id}
DELETE - https://rm9l6gpxpi.execute-api.us-east-1.amazonaws.com/dev/user/contacts/{contact_id}
'''