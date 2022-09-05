
def custom_response(status_code, message):
    return {"status_code": status_code, "message": message}


def update_response(message="Updated Successfully"):
    return {"status_code": 200, "message": message}


def get_response(message="Get Successful"):
    return {"status_code": 200, "message": message}


def create_response(message="Created Successfully"):
    return {"status_code": 201, "message": message}


def delete_response(message="Deleted Successfully", *args, **kwargs):
    return {"status_code": 204, "message": message}


def bad_request(message="Bad Request"):
    return {"status_code": 400, "message": message}


def unauthorised_response(message="Unauthorised"):
    return {"status_code": 401, "message": message}


def access_denied_response(message="Access Denied, Forbidden"):
    return {"status_code": 403, "message": message}


def resource_not_found(message="Requested resource not found"):
    return {"status_code": 404, "message": message}


def internal_server_error(message="Internal Server Error"):
    print("[LUMIGO_LOG]", message)
    return {"status_code": 500, "message": message}
