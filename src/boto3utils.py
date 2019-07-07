###############
#
# boto3 utils
#
###############

import sys
import boto3
from botocore.exceptions import ClientError


def upload_to_bucket(to_upload, uploaded_name, bucket_name, logger=None):
    """
    Simple utility to upload a given file to provided S3 bucket.

    To be used from the command line or in notebooks for easy access.

    Args:
        to_upload (str): Absolute path to file.
        uploaded_name (str): Name for the uploaded file in the s3 bucket. Must be unique for the bucket.
        bucket_name (str): Name of bucket to upload to
        logger (Logger):

    Returns:
        (bool) True if successful, False otherwise.
    """

    try:
        s3 = boto3.resource('s3')

        data = open(to_upload, 'rb')
        s3.Bucket(bucket_name).put_object(Key=uploaded_name, Body=data)

        if logger:
            logger.info(f"Successfully uploaded file: {to_upload} to bucket={bucket_name}")
        return True

    except Exception as e:
        if logger:
            logger.warning(f"Failed to upload file to bucket")

        return False


def start_instance(instance_id, logger=None):
    """
    Utility to test and start an existing EC2 instance.
    
    Args:
        instance_id (str):
        logger (Logger):

    Returns:
        (bool) True if successful, False otherwise.
    """
    ec2 = boto3.client('ec2')

    # Do a dryrun first to verify permissions
    try:
        ec2.start_instances(InstanceIds=[instance_id], DryRun=True)
        if logger:
            logger.info(f"Dryrun to start instance_id={instance_id} successful")

    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            if logger:
                logger.warning(f"Dryrun to start instance_id={instance_id} failed with error: {str(e)}")
            raise

    # Dry run succeeded, run start_instances without dryrun
    try:
        response = ec2.start_instances(InstanceIds=[instance_id], DryRun=False)
        if logger:
            logger.info(f"{response}")

        return True
    except ClientError as e:
        if logger:
            logger.warning(f"Actual startup for instance_id={instance_id} failed with error: {str(e)}")
        return False


def stop_instance(instance_id, logger=None):
    """

    Args:
        instance_id (str):
        logger (Logger):

    Returns:
        (bool) True if successful, False otherwise.
    """
    ec2 = boto3.client('ec2')

    # Do a dryrun first to verify permissions
    try:
        ec2.stop_instances(InstanceIds=[instance_id], DryRun=True)
        if logger:
            logger.info(f"Dryrun to stop instance_id={instance_id} successful")

    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            if logger:
                logger.warning(f"Dryrun to stop instance_id={instance_id} failed with error: {str(e)}")
            raise

    # Dry run succeeded, run start_instances without dryrun
    try:
        response = ec2.stop_instances(InstanceIds=[instance_id], DryRun=False)
        if logger:
            logger.info(f"{response}")

        return True
    except ClientError as e:
        if logger:
            logger.warning(f"Actual stopping for instance_id={instance_id} failed with error: {str(e)}")
        return False
