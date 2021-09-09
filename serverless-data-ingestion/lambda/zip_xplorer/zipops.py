from zipfile import ZipFile

from smart_open import smart_open


def analyse_zip_files(bucket, csize_, zips):
    files_ = []
    for zip_ in zips:
        files_.extend(check_zip_file(bucket, csize_, zip_))

    return files_


def check_zip_file(bucket, csize_, zfile):
    s3_uri = f"s3://{bucket}/{zfile}"
    with smart_open(s3_uri, 'rb') as zip_obj:
        zippo = ZipFile(zip_obj)

        return [
            {
                "zip": zfile,
                "chunks": csize_,
                "file": file_,
                "bucket": bucket,
            } for file_ in zippo.namelist() if file_.endswith('.csv')
        ]