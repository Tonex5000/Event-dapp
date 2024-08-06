from os import environ
import logging
import requests
import json
import binascii

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

# Global dictionary to store events
events = {}

def encode_response(response_dict):
    json_str = json.dumps(response_dict)
    hex_str = binascii.hexlify(json_str.encode()).decode()
    return f"0x{hex_str}"

def handle_advance(data):
    logger.info(f"Received advance request data {data}")
    try:
        payload = data['payload']
        
        # Ensure payload is a string and remove '0x' prefix if present
        if isinstance(payload, str):
            payload = payload[2:] if payload.startswith('0x') else payload
        else:
            raise ValueError("Payload must be a string")

        # Convert the hexadecimal string to bytes, then to a UTF-8 string
        payload_str = bytes.fromhex(payload).decode('utf-8')
        
        # Parse the JSON string
        event_data = json.loads(payload_str)
        
        action = event_data["action"]

        if action == "create_event":
            event_id = len(events) + 1
            events[event_id] = {
                "name": event_data["name"],
                "date": event_data["date"],
                "capacity": int(event_data["capacity"]),
                "registered": 0
            }
            result = {"status": "accept", "message": f"Event created with ID: {event_id}"}
        elif action == "register":
            event_id = int(event_data["event_id"])
            if event_id in events:
                if events[event_id]["registered"] < events[event_id]["capacity"]:
                    events[event_id]["registered"] += 1
                    result = {"status": "accept", "message": "Registration successful"}
                else:
                    result = {"status": "reject", "message": "Event is full"}
            else:
                result = {"status": "reject", "message": "Event not found"}
        else:
            result = {"status": "reject", "message": "Invalid action"}

        return encode_response(result)

    except Exception as e:
        logger.error(f"Error processing advance request: {e}")
        error_result = {"status": "reject", "message": str(e)}
        return encode_response(error_result)

def handle_inspect(data):
    logger.info(f"Received inspect request data {data}")
    try:
        # Check if data is already a dictionary
        if isinstance(data, dict):
            decoded_data = data
        else:
            # If it's a string (possibly hex-encoded), decode it
            if isinstance(data, str):
                if data.startswith('0x'):
                    data = data[2:]
                # Convert hex to bytes, then to string, then parse JSON
                decoded_data = json.loads(bytes.fromhex(data).decode('utf-8'))
            else:
                raise ValueError("Unexpected data type for inspect request")

        action = decoded_data.get("action")

        if action == "get_event":
            event_id = int(decoded_data["event_id"])
            if event_id in events:
                result = {"status": "accept", "data": events[event_id]}
            else:
                result = {"status": "reject", "message": "Event not found"}
        elif action == "list_events":
            result = {"status": "accept", "data": events}
        else:
            result = {"status": "reject", "message": "Invalid action"}

        return encode_response(result)

    except Exception as e:
        logger.error(f"Error processing inspect request: {e}")
        error_result = {"status": "reject", "message": f"Error processing request: {str(e)}"}
        return encode_response(error_result)

handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}

while True:
    logger.info("Sending finish")
    response = requests.post(rollup_server + "/finish", json={"status": "accept"})
    logger.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        handler = handlers[rollup_request["request_type"]]
        result = handler(rollup_request["data"])
        response = requests.post(rollup_server + "/report", json={"payload": result})
        logger.info(f"Received report status {response.status_code}")