from boto3 import resource
from boto3.dynamodb.conditions import Key
import json


resource = resource('dynamodb')

def create():
   table = resource.create_table(
       TableName = 'Employee', # Name of the table
       KeySchema = [
           {
               'AttributeName': 'id',
               'KeyType'      : 'HASH'
           },
           {
               'AttributeName': 'name',
               'KeyType': 'RANGE'
           }
       ],
       AttributeDefinitions = [
           {
               'AttributeName': 'id',
               'AttributeType': 'S'
           },
           {
               'AttributeName': 'name',
               'AttributeType': 'S'
           }
       ],
       ProvisionedThroughput={
           'ReadCapacityUnits'  : 1,
           'WriteCapacityUnits': 1
       }
   )
   return table

Table = resource.Table('Employee')

def write(id, name, workingdays):
   response = Table.put_item(
       Item = {
           'id'     : id,
           'name'  : name,
           'workingdays' : workingdays
       }
   )
   return response


def read(id):
   response = Table.query(
    KeyConditionExpression=Key('id').eq(id)
   )
   items = response['Items']
   if items:
       return items[0]
   else:
       return {'msg': 'Item does not exist'}


def update(id: str, data: dict):
    response = Table.update_item(
        Key={
            'id': str(id),
            'name': str(data['name'])
        },
        AttributeUpdates={
            'workingdays': {
                'Value': data['workingdays'],
                'Action': 'PUT'
            }
        },

        ReturnValues="UPDATED_NEW"
    )
    return response


def delete(id):
    data=read(id)
    response = Table.delete_item(
        Key={
            'id': str(id),
            'name': str(data['name'])
        }
    )
    return response