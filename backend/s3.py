import boto3

def create_s3_bucket(aws_access_key, aws_secret_key, bucket_name, region):
    # Create an S3 client
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key,
                             aws_secret_access_key=aws_secret_key,
                             region_name=region)

    # Create the S3 bucket
    try:
        s3.create_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' created successfully!")
    except Exception as e:
        print(f"Error creating bucket: {e}")

def upload_file_to_s3(aws_access_key, aws_secret_key, bucket_name, file_name, file_content, region):
    # Create an S3 client
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key,
                             aws_secret_access_key=aws_secret_key,
                             region_name=region)

    # Upload the file to the S3 bucket
    try:
        s3.put_object(Body=file_content, Bucket=bucket_name, Key=file_name)
        print(f"File '{file_name}' uploaded successfully!")
    except Exception as e:
        print(f"Error uploading file: {e}")