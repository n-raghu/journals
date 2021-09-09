import csv
import time
import json
import boto3
import codecs
from zipfile import ZipFile

from smart_open import smart_open

cln_dynamodb = boto3.client('dynamodb')
rsc_dynamodb = boto3.resource('dynamodb')


def create_db_tab(col, db_keys, client_=cln_dynamodb, rsc_=rsc_dynamodb):
    create_response = False
    partition_key = db_keys.get('partition_key', None)
    if not partition_key:
        raise Exception('Partition Key not found')
    partition_key_type = db_keys.get('partition_key_type', None)

    attributes_def = [
        {
            'AttributeName': partition_key,
            'AttributeType': partition_key_type
        }
    ]
    key_schema = [
        {
            'AttributeName': partition_key,
            'KeyType': 'HASH'
        }
    ]

    range_key = db_keys.get('range_key', None)
    if range_key:
        range_key_type = db_keys.get('range_key_type', None)
        attributes_def.append(
            {
                'AttributeName': range_key,
                'AttributeType': range_key_type,
            }
        )
        key_schema.append(
            {
                'AttributeName': range_key,
                'KeyType': range_key_type
            }
        )

    try:
        response = client_.create_table(
            AttributeDefinitions=attributes_def,
            KeySchema=key_schema,
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 10,
            },
            TableName=col,
        )
        
        for _ in range(10):
            time.sleep(3)
            if rsc_.describeTable(col).status == 'active':
                create_response = True
                print('Table created Successfully')
                break
        if not create_response:
            raise Exception('Took Long time to create collection')

    except client_.exceptions.ResourceInUseException:
        print('Table Exists', flush=True)
        create_response = True

    return create_response


def read_json(s3_uri, key):
    with smart_open(s3_uri, 'rb') as zip_obj:
        zippo = ZipFile(zip_obj)
        json_file = key.split('.')[0] + '.json'
        with zippo.open(json_file, 'r') as jfile:
            doc = json.loads(jfile.read())

    return doc


def write_to_dynamo(table_name, rows, rsc_dynamodb=rsc_dynamodb):

    table = rsc_dynamodb.Table(table_name)

    with table.batch_writer(overwrite_by_pkeys=['uid']) as batch:
        for row in rows:
            batch.put_item(Item=row)


def yield_csv_data(s3_uri, key):
    with smart_open(s3_uri, 'rb') as zip_obj:
        zippo = ZipFile(zip_obj)
        with zippo.open(key, 'r') as csv_file:
            for row in csv.DictReader(codecs.iterdecode(csv_file,'utf-8'), delimiter='|'):
                yield row
