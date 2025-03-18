#!/usr/bin/env python3
from sys import stdin, stderr
import json
import requests
import logging

# Load config from semaphore_config file
with open('semaphore_config.json') as config_file:
    config = json.load(config_file)

logging_level = getattr(logging, config.get('logging_level', 'INFO').upper(), logging.INFO)
# Create a custom StreamHandler that flushes immediately
class FlushStreamHandler(logging.StreamHandler):
    def emit(self, record):
        super().emit(record)
        self.flush()

# Configure logging to use the custom handler
logging.basicConfig(level=logging_level, handlers=[FlushStreamHandler(stderr)])

semaphore_url = config['semaphore_url']
token = config['token']

# Get the values we got from the URL (stdin)
# In NocoDB:
# CONCAT("https://smdadminprod01.urmc-sh.rochester.edu/TW/noco2semaphore/{semaphore_integration}/", {Id})

data = json.loads(stdin.read())
# Test if path is in the data
if 'path' not in data or not data['path']:
    print("No path in data", file=stderr)
    exit(1)

if not token:
    print("No token in config", file=stderr)
    exit(2)

if not semaphore_url:
    print("No semaphore_api_url in config", file=stderr)
    exit(3)

path = data['path']
path_parts = path.split('/')
semaphore_integration = path_parts[0]
noco_id = path_parts[1]

# Create a data object
data_object = {
  "type": "records.after.trigger",
  "data": {
    "rows": [
      {
        "Id": noco_id,
      }
    ]
  }
}

# Define the Authorization header
headers = {
    "Authorization": f"{token}"
}

# Call the Semaphore API with that ID
response = requests.post(f"{semaphore_url}/api/integrations/{semaphore_integration}", json=data_object, headers=headers)
logging.debug(f"URL: {response.request.url}")
logging.info(f"Status Code: {response.status_code}")
logging.debug(f"Response: {response.text}")
# Print redirect URL to stdout
print(json.dumps({"redirect_url_success": f"{semaphore_url}/project/{config['project']}/templates/{config['template']}/tasks"}))
# Return a 0 exit code
exit(0)