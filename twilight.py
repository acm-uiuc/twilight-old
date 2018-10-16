# Evan Widloski - 2018-10-15
# Skeleton Flask App for Twilight
from flask import Flask, request, make_response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(message)s')

app = Flask(__name__)
limiter = Limiter(app, key_func=lambda: request.headers.get('token'))

# schema for POSTed json - will be more complicated once we spec it out
schema = {
    "type": "object",
    "properties":{
        "abc" : {"type": "number"}
    }
}

@app.route('/', methods=['POST'])
@limiter.limit("2/minute")
def hello():
    """POST endpoint for JSON data"""

    token = request.headers.get('token')

    if validate_token(token):
        logging.info("Validated token: {}".format(token))
        try:
            j = json.loads(request.get_data())
            validate(j, schema)
        except json.JSONDecodeError:
            logging.info("JSON parsing error")
            return "Invalid json\n"
        except ValidationError as e:
            logging.info("JSON validation error")
            return "JSON Validation error at \"{}\": {}\n".format('/'.join(e.path), e.message)

        return "Success\n"
    else:
        logging.info("Invalid token: {}".format(token))
        return "Invalid token\n"


def validate_token(token):
    """Groot auth stuff goes here"""

    return True if token == 'foo' else False


@app.errorhandler(429)
def ratelimit(e):
    """Custom response for rate limit exceeded"""

    return make_response("Rate limit exceeded: {}\n".format(e.description), 429)
