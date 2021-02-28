import logging
import os
from ariadne import graphql_sync
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, request, jsonify
from resolvers import schema

app = Flask(__name__)


@app.route('/graphql', methods=['GET'])
def playground():
    return PLAYGROUND_HTML, 200


@app.route('/graphql', methods=['POST'])
def graphql_server():
    data = request.get_json()
    app.logger.info(f"Request: {data}")
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    status_code = 200 if success else 400
    app.logger.info(f"Response: ({status_code}) {result}")
    return jsonify(result), status_code


if __name__ != "__main__":
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_ENV") == "dev"
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    app.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
