import json
import base64
import os
import boto3

s3_client = boto3.resource('s3')
s3_bucket_name = "tbsm-kinesis-etl-bucket"  # Replace with your bucket name

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))

    for record in event['Records']:
        encoded_data = record['kinesis']['data']
        decoded_bytes = base64.b64decode(encoded_data)
        decoded_string = decoded_bytes.decode("utf-8")

        print(f"Decoded data: {decoded_string}")

        sequence_number = record['kinesis']['sequenceNumber']
        s3_file_name = f"{sequence_number}.json"
        local_file_path = f"/tmp/{s3_file_name}"

        with open(local_file_path, 'w') as f:
            json.dump(json.loads(decoded_string), f)

        print(f"Saving file locally: {local_file_path}")

        s3_client.meta.client.upload_file(local_file_path, s3_bucket_name, s3_file_name)
        print(f"Uploaded {s3_file_name} to S3 bucket {s3_bucket_name}")

        os.remove(local_file_path)
        print(f"Deleted local file {local_file_path}")

    return {
        'statusCode': 200,
        'body': json.dumps('Processing complete')
    }
