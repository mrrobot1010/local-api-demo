import controller as dynamodb
from flask import request, Flask
from flask_restful import Api
from flask_httpauth import HTTPBasicAuth
import boto3
import json

app = Flask(__name__)
api = Api(app, prefix="/api/v1")
auth = HTTPBasicAuth()
dynamodb_client = boto3.client('dynamodb')

USER_CREDS = {
    "admin": "SuperAdmin@Pwd"
}
@auth.verify_password
def verify(usr,pwd):
    if not usr and pwd:
        return False
    return USER_CREDS.get(usr) == pwd

@app.route('/')
@auth.login_required
def root_route():
    table_name = 'Employee'
    existing_tables = dynamodb_client.list_tables()['TableNames']

    if table_name not in existing_tables:
        dynamodb.create()
        return 'Table created'
    else:
        return 'Table Already exists'

@app.route('/dev/employee/create', methods=['POST'])
@auth.login_required
def create_data():
    input = list(request.get_json())

    for data in input:
        response = dynamodb.write(data['id'], data['name'], data['workingdays'])

    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
                'msg': 'Add successful'
            }
    return {
            'msg': 'error occurred',
            'response': response
        }

@app.route('/dev/employee/list', methods=['GET'])
@auth.login_required
def get_data():
    id = request.args.get('id')
    data=(id.split(","))
    response=[]
    for val in data:
        tmp_response = (dynamodb.read(str(val)))
        response.append(tmp_response)
    return json.dumps(response)

@app.route('/dev/employee/delete', methods=['DELETE'])
@auth.login_required
def delete_data():
    id = request.args.get('id')
    data = (id.split(","))

    for val in data:
        response = dynamodb.delete(str(val))

    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
                'msg': 'Delete successful'
            }
    return {
            'msg': 'error occurred',
            'response': response
        }

@app.route('/dev/employee/update', methods=['PUT'])
@auth.login_required
def update_data():
    input = request.get_json()

    for data in input:
        response = dynamodb.update(str(data['id']), data)
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
                'msg': 'update successful'
            }
    return {
            'msg': 'error occurred',
            'response': response
        }

if __name__ == '__main__':
    app.run(debug=True, port=5000)