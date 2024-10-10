import boto3

def instance_launch(aws_access_key_id, aws_secret_access_key, region_name, instance_type, image_id):
    try:
        myec2 = boto3.resource(
            service_name="ec2",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

        ec2 = myec2.create_instances(
            InstanceType=instance_type,
            ImageId=image_id,
            MaxCount=1,
            MinCount=1
        )
        instance_id = ec2[0].id
        return True, f"Instance launched successfully! Instance ID: {instance_id}"
    except Exception as e:
        return False, str(e)
