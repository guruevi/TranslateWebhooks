#!/usr/bin/env python3
#-*- coding: utf-8 -*-
# Description: This script is used to translate any URL call from one place and redirect to another

import json
import logging
import subprocess
from flask import Flask, request, redirect, send_from_directory

app = Flask(__name__)

# Load routes from config file
with open('config.json') as config_file:
    config = json.load(config_file)

logging_level = getattr(logging, config.get('logging_level', 'INFO').upper(), logging.INFO)
logging.basicConfig(level=logging_level)

sub_path = config.get('proxy_path', '')


def call_webhook(script, data):
    result = subprocess.run(['python3', script], input=json.dumps(data), text=True, capture_output=True, cwd='scripts')
    logging.debug(result.stdout)
    logging.info(result.stderr)
    logging.debug(result.returncode)

    try:
        parsed_output = json.loads(result.stdout)
    except json.JSONDecodeError:
        parsed_output = {}

    return result.returncode, parsed_output


# Dynamically create routes
for route_config in config['routes']:
    def create_route(route):
        def handle_webhook(path):
            data = request.get_data(as_text=True)
            query_params = request.args.to_dict()
            logging.debug(f"Data: {data}")
            logging.debug(f"Path: {path}")
            logging.debug(f"Query params: {query_params}")
            combined_data = {
                "data": data,
                "path": path,
                "query_params": query_params
            }
            logging.debug(f"Combined Data: {combined_data}")
            rc, output = call_webhook(route['webhook_script'], combined_data)
            if rc == 0:
                logging.info(f"Webhook success: {route['webhook_script']}")
                if "redirect_url_success" in output:
                    return redirect(output['redirect_url_success'])

                # By default, we use the config
                return redirect(route['outgoing_url_success'])
            else:
                logging.error(f"Webhook failed: {route['webhook_script']}")
                if "redirect_url_failure" in output:
                    return redirect(output['redirect_url_failure'])

                # By default, we use the config
                return redirect(route['outgoing_url_failure'])

        return handle_webhook


    app.add_url_rule(f'{sub_path}/{route_config["incoming_url"]}/<path:path>', view_func=create_route(route_config))


# Serve static files
@app.route('/static/<filename>')
def serve_static(filename):
    return send_from_directory('static', filename + '.html')


if __name__ == '__main__':
    app.run(port=config.get('port', 5001), debug=(logging_level == logging.DEBUG))
