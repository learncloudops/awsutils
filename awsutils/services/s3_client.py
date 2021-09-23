from typing import List
import os
import boto3
from botocore.exceptions import ClientError

from awsutils.services import Validate

class S3Client(object):
    '''
        a basic abstraction of the boto3 client for
        Amazon S3. Provides convenience to execute
        the common S3 functions used in an application.
    '''

    def __init__(self, region_name:str="us-east-1"):
        '''
            constructor
            :params:
                region_name (str) - the amazon region. Defaults to us-east-1
        '''
        Validate.not_empty(region_name, 'Region name cannot be null')
        self.client = boto3.client("s3", region_name=region_name)


    def list_buckets(self) -> List:
        '''
            Gets a list of the bucket names in your account
            :params:
                None
            :returns:
                the list of bucket names as strings
        '''
        response = self.client.list_buckets()
        return [bucket["Name"] for bucket in response["Buckets"]]


    def list_object_names(self, bucket_name:str, prefix:str, max_results=1000) -> List:
        '''
            Lists the names of the first 1000 records in the prefix.
            :params:
                bucket_name (str): the bucket name
                prefix (str): the root key (or folder) where the files exist
                max_results (int): the number of names to return (max 1000)
            :return:
                a list of the object keys from the prefix
        '''
        if max_results > 1000:
            raise ValueError('list_object_names only supports up to 1000 results')
        Validate.not_empty(bucket_name, 'bucket name cannot be empty')
        Validate.not_empty(prefix, 'prefix cannot be empty')

        response = self.client.list_objects_v2(
            Bucket=bucket_name,
            Prefix=prefix,
            MaxKeys=max_results
        )
        return [object["Key"] for object in response["Contents"]]


    def download_object(self, bucket_name:str, 
                        prefix:str, local_folder:str, 
                        local_file:str) -> None:
        '''
            Downloads a single object from a bucket
            :params:
                bucket_name (str) - the bucket name
                prefix (str) - the object path in S3
                local_folder (str) - the folder on the local disk where the file was written
                local_file (str) - the name of the file on disk
            :return:
                None
        '''
        Validate.not_empty(bucket_name, 'bucket name cannot be empty')
        Validate.not_empty(prefix, 'prefix cannot be empty')
        Validate.not_empty(local_folder, 'local folder cannot be empty')
        Validate.not_empty(local_file, 'local file name cannot be empty')
        os.makedirs(local_folder, exist_ok=True)
        self.client.download_file(
            Bucket=bucket_name,
            Key=prefix,
            Filename=f'{local_folder}/{local_file}')


    def put_object(self, bucket_name: str, key: str, local_file:str) -> None:
        '''
            Put an object to a bucket
            :params:
                bucket_name (str) - the bucket name
                key (str) - the path in S3 where to write the object
                local_file (str) - the path to the file on disk
            :return:
                None
        '''
        Validate.not_empty(bucket_name, 'bucket name cannot be empty')
        Validate.not_empty(key, 'key cannot be empty')
        Validate.not_empty(local_file, 'local fille name cannot be empty')
        self.client.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=open(local_file, 'rb')
        )
