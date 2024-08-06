# Python DApp Template

# Event Management System

This is a simple event management system implemented as a rollup application. It allows users to create events, register for events, and retrieve event information.

## Features

- Create new events with a name, date, and capacity
- Register for existing events
- Get information about a specific event
- List all events

## Getting Started
Follow the instruction below to get started.

## Prerequisites
Here are some packages you need to have installed on your PC:

nodejs, npm, yarn

docker

cartesi-cli

npm install -g @cartesi/cli

## Usage

The application is designed to run as a rollup, interacting with a rollup server. To run the application:

1. Set the environment variable `ROLLUP_HTTP_SERVER_URL` to the URL of your rollup server.
2. Run the script: python event_management_system.py

## API

The system supports two types of requests: advance and inspect.

### Advance Requests

Advance requests are used to modify the state of the system.

1. Create Event:
```json
{
  "action": "create_event",
  "name": "Event Name",
  "date": "YYYY-MM-DD",
  "capacity": "100"
}
```



Register for Event:
```json
{
  "action": "register",
  "event_id": "1"
}
```

### Inspect Requests

Inspect requests are used to retrieve information without modifying the state.

Get Event Information:
```json
{

  "action": "get_event",
  "event_id": "1"
}
```

List All Events:
```json
{
  "action": "list_events"
}
```

## Error Handling
The system includes error handling for various scenarios, such as invalid actions, full events, or non-existent events. Error messages are returned in the response payload.

## Logging
The system uses Python's built-in logging module to log information about requests, responses, and any errors that occur during operation.

## Contributing
Contributions to improve the system are welcome. Please submit a pull request or open an issue to discuss proposed changes.
