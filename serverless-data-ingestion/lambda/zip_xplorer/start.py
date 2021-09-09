import csv
import json
import time
import boto3
import codecs
import itertools

from smart_open import smart_open

from zipops import analyse_zip_files


def handler(event, context):

    bucket = event['body']['bucket']
    all_zips = event['body']['files']
    chunks = event['body']['chunks']
    all_files = analyse_zip_files(bucket, chunks, all_zips)

    return {
        "statusCode": 200,
        "body": {
            "bucket": bucket,
            "zip_files": all_zips,
            "files": all_files
        }
    }
