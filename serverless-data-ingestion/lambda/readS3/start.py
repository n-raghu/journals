import os
import boto3


def handler(event, context):

    bucket = os.environ['bucket']
    file_xtn = '.zip'
    B = boto3.resource('s3').Bucket(bucket)
    all_zips = list(obj.key for obj in B.objects.all() if obj.key.endswith(file_xtn))

    return {
        'statusCode': 200,
        'body': {
            'bucket': bucket,
            'files': all_zips,
            'chunks': os.environ['chunks']
        }
    }
