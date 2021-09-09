import itertools

from dataops import read_json, create_db_tab, yield_csv_data, write_to_dynamo


def handler(event, context):

    bucket = event['bucket']
    chunks = int(event['chunks'])
    s3_uri = f"s3://{bucket}/{event['zip']}"
    collection = event['file']

    csize = 10
    col_ = collection.split('.')[0]
    col_name = col_.strip().split('/')[-1:][0]

    db_keys = read_json(s3_uri, collection)

    db_tab = create_db_tab(col_name, db_keys)

    if not db_tab:
        exc = {
            'statusCode': 422,
            'body': {
                'err': f'Unable to create Collection {collection}'
            }
        }
        raise Exception(exc)

    stream = yield_csv_data(s3_uri, collection)
    response = []

    if chunks == -1:
        while True:
            chunk = list(itertools.islice(stream, csize))
            if not chunk:
                break
            write_to_dynamo(col_name, chunk)
    elif chunks > 0:
        for _ in range(chunks):
            chunk = list(itertools.islice(stream, csize))
            write_to_dynamo(col_name, chunk)
    else:
        raise Exception("Not an acceptable value of chunk")

    return {
        "statusCode": 200,
        "body": {
            "bucket": bucket,
            "source": s3_uri,
            "chunks": chunks,
            "chunk_si": csize,
        }
    }
