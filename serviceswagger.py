from nycaddress import parse
from flask import Flask, request, jsonify
from flask_swagger import swagger

# from flask.ext.cors import CORS
# CORS(app, resources=r'/*', allow_headers='Content-Type')

app = Flask(__name__)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         "Authorization, Content-Type")
    response.headers.add('Access-Control-Expose-Headers', "Authorization")
# "GET, POST, PUT, DELETE, OPTIONS")
    response.headers.add('Access-Control-Allow-Methods',
                         "GET, POST")
    response.headers.add('Access-Control-Allow-Credentials', "true")
    response.headers.add('Access-Control-Max-Age', 60 * 60 * 24 * 20)
    return response


def parseAddresses(text):
    return jsonify({'addresses':
                    [{"text": loc} for loc in parse(text)]})


@app.route('/', methods=['GET'])
def index():
    return "BetaNYC 5 Borough's address finder"


@app.route('/api/parseaddresses', methods=['POST'])
def parseaddresses():
    """
    Parse Addresses
    The only endpoint used to submit a string to be parsed.
    ---
    responses:
        '200':
            description: list of addresses.
            schema:
                id: StreetAddress
                required:
                    - text
                properties:
                    text:
                        type: string
                        description: Fulltext US street address
        default:
            description: Unexpected error
            schema:
                id: Error
                required:
                    - code
                    - message
                properties:
                    code:
                        type: integer
                        format: int32
                    message:
                        type: string
                        description: Error message

    parameters:
        - in: body
          name: source
          schema:
              required:
                  - source
              id: Input
              properties:
                  source:
                      type: string
                      description: String to parse
    """
    if request.method == 'GET':
        return 'So, instructions would be printed here...'

    data = request.json
    data = data['source']
    print 'data is %s' % data
    return parseAddresses(data)


@app.route('/spec')
def spec():
    swag = swagger(app)
    swag['info']['version'] = '0.1'
    swag['info']['title'] = "BetaNYC 5 Borough's address finder"
    return jsonify(swag)


@app.route('/api')
def apiroot():
    return app.send_static_file('index.html')


@app.route('/api/<path:path>')
def api(path):
    return app.send_static_file(path)

if __name__ == '__main__':
    app.run(debug=True)
