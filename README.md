# Flask Webhook Proxy

This project is a Flask application that acts as a proxy for handling webhooks. It dynamically creates routes based on a
configuration file and can redirect users to specified URLs or chain into more scripts.

## Features

- Dynamic route creation based on configuration
- Error handling with custom error pages
- Docker support for containerization

## Requirements

- Python 3.9+
- Flask
- Requests

## Installation

1. Clone the repository:
    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Configuration

### `config.json`

This file contains the main configuration for the Flask application.

Example:
```json
{
  "proxy_path": "/TW",
  "logging_level": "DEBUG",
  "port": 5001,
  "routes": [
    {
      "incoming_url": "n2s",
      "methods": ["GET","POST"],
      "webhook_script": "scripts/noco2semaphore.py",
      "outgoing_url_success": "/static/200",
      "outgoing_url_failure": "/static/500"
    }
  ]
}
```

- `proxy_path`: The base path if you are behind a reverse proxy.
- `routes`: A list of dictionaries containing the following keys:
- `incoming_url`: The URL path to listen for.
- `methods`: The HTTP methods to listen for.
- `webhook_script`: The script to run when the webhook is received.
- `outgoing_url_success`: The URL to redirect to if the script is successful.
- `outgoing_url_failure`: The URL to redirect to if the script fails.

The webhook script will receive a JSON with the following data:
```json
{
    "data": "string",
    "path": "string",
    "query_params": "string"
}
```
- data: The data sent from the webhook (eg. POST or form data - in string format)
- path: The path after the webhook URL (eg. if you call /n2s/project/123, this will be project/123)
- query_params: The query parameters sent with the webhook (eg. ?param1=value1&param2=value2)

## Running the Application

1. Start the Flask application:
    ```sh
    python app.py
    ```

2. The application will be available at `http://localhost:5001` (or the port specified in `config.json`).

## Docker

To run the application in a Docker container:

1. Build the Docker image:
    ```sh
    docker build -t flask-webhook-proxy .
    ```

2. Run the Docker container:
    ```sh
    docker run -p 5000:5000 flask-webhook-proxy
    ```

## Static Pages

You can set static pages for generic error handling. See the following files:

- `static/404.html`
- `static/500.html`
- `static/200.html`

## Logging

Logging is configured to output to `stderr` with immediate flushing to ensure logs are not cached.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.