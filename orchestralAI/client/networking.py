import json
import uuid

from ..exceptions import RemoteActionException
from ..websocket_client import WebSocketClient
from .connector import connect_client


# Networking Functions
async def run_action(wsc: WebSocketClient, action: str, **kwargs):
    # Prepare request
    request = {
        "request_id": str(uuid.uuid4()),
        "action": action,
        "parameters": kwargs,
    }
    json_request = json.dumps(request)

    # Make request
    await wsc.send_message(json_request)
    while True:
        json_response = await wsc.receive_message()

        # Decode response
        response = json.loads(json_response)
        if not response:
            continue
        
        # Validate request id
        if response["request_id"] != request["request_id"]:
            continue

        # Return results
        result = response["result"]
        success = response["success"]
        if success:
            return result
        else:
            raise RemoteActionException(str(result))


async def get_connection(api_key: str):
    """Establishes a websocket connection"""
    wsc = await connect_client(api_key)
    return wsc


# Utility Functions
def secure_json_decode(json_string):
    try:
        data = json.loads(json_string)
        validate_json_structure(data)
    except (json.JSONDecodeError, AssertionError):
        return False
    
    return data

def validate_json_structure(data):
    """Enforce structure of websocket JSON request here"""
    assert isinstance(data["request_id"], str)
    assert isinstance(data["action"], str)
    assert isinstance(data["parameters"], dict)