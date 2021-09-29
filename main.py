# Copyright 2019 Google, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START cloudrun_imageproc_controller]
# [START run_imageproc_controller]
import base64
import json
import os
import requests


from flask import Flask, request
from google.cloud import storage


app = Flask(__name__)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    storage_client = storage.Client()
    blobs = storage_client.list_blobs("mxm-predeng-input")
    csstring = ""

    for blob in blobs:
        csstring += str(blob.name)
    api_key = os.environ.get('OPENSKY')
    city = "Nashville"
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(city, api_key)
    openstr = ""
    try:
        r = requests.get(url)
        r_data = r.json()
        openstr = str(r_data)

    except Exception as err:
        print(f'Other error occurred: {err}')

    return 'Input File List' + csstring + "\nOpenSkyData: " + openstr

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )


def download_blob(bucket_name, source_blob_name, destination_file_name):
    # bucket_name = "your-bucket-name"
    # source_blob_name = "storage-object-name"
    # destination_file_name = "local/path/to/file"
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print(
        "Downloaded storage object {} from bucket {} to local file {}.".format(
            source_blob_name, bucket_name, destination_file_name
        )
    )


def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs("mxm-predeng-input")
    return str(blobs)
#    for blob in blobs:
#        print(blob.name)


if __name__ == "__main__":
    PORT = int(os.getenv("PORT")) if os.getenv("PORT") else 8080

    # This is used when running locally. Gunicorn is used to run the
    # application on Cloud Run. See entrypoint in Dockerfile.
    app.run(host="127.0.0.1", port=PORT, debug=True)
