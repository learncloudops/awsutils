from tempfile import NamedTemporaryFile
from awsutils.services import S3Client

import pytest
from awsutils.services import S3Client
import os

BUCKET_NAME = 's3_test_bucket'

@pytest.fixture
def bucket_name():
  return BUCKET_NAME
 
  
@pytest.fixture
def s3_test(s3_client, bucket_name):
  s3_client.create_bucket(Bucket=bucket_name)
  yield


def test_list_buckets(s3_client, s3_test):
  s3 = S3Client()
  buckets = s3.list_buckets()
  buckets == [BUCKET_NAME]


def test_list_object_names_max_result_greater_than_1000(s3_client, s3_test):
  s3 = S3Client()
  with pytest.raises(ValueError):
    s3.list_object_names(bucket_name=BUCKET_NAME,
                         prefix='file1', max_results=5000)


def test_list_object_names_prefix_not_none(s3_client, s3_test):
  s3 = S3Client()
  with pytest.raises(ValueError):
    s3.list_object_names(bucket_name=BUCKET_NAME,
                         prefix=None)


def test_list_object_names_bucket_name_not_none(s3_client, s3_test):
  s3 = S3Client()
  with pytest.raises(ValueError):
    s3.list_object_names(bucket_name=None,
                         prefix='file1')


def test_list_object_names(s3_client, s3_test):
  file_body = 'test'
  with NamedTemporaryFile(delete=True, suffix='.txt') as tmp:
    with open(tmp.name, 'w', encoding='UTF-8') as f:
      f.write(file_body)

    s3_client.upload_file(tmp.name, BUCKET_NAME, 'file1')
    s3_client.upload_file(tmp.name, BUCKET_NAME, 'file2')
  
  s3 = S3Client()
  objects = s3.list_object_names(bucket_name=BUCKET_NAME, prefix='file1')
  assert objects == ['file1']

def test_download_object(s3_client, s3_test):
  file_body = 'test'
  
  s3_client.put_object(Bucket=BUCKET_NAME, 
                       Key="file1.txt",
                       Body=(open('tests/sample.txt', 'rb')))

  s3 = S3Client()
  s3.download_object(bucket_name=BUCKET_NAME, prefix='file1.txt',
                     local_folder='/tmp', local_file='file1.txt')
  assert os.path.isfile('/tmp/file1.txt')


def test_download_object_bucket_name_not_null(s3_client, s3_test):
  s3 = S3Client()
  with pytest.raises(ValueError):
    s3.download_object(bucket_name=None, prefix='aa', 
                      local_folder='aa', local_file='aa')


def test_download_object_prefix_not_null(s3_client, s3_test):
  s3 = S3Client()
  with pytest.raises(ValueError):
    s3.download_object(bucket_name=BUCKET_NAME, prefix=None,
                       local_folder='aa', local_file='aa')


def test_download_object_local_folder_not_null(s3_client, s3_test):
  s3 = S3Client()
  with pytest.raises(ValueError):
    s3.download_object(bucket_name=BUCKET_NAME, prefix='aa',
                       local_folder=None, local_file='aa')


def test_download_object_local_file_not_null(s3_client, s3_test):
  s3 = S3Client()
  with pytest.raises(ValueError):
    s3.download_object(bucket_name=BUCKET_NAME, prefix='aa',
                       local_folder='aa', local_file=None)


def test_put_object(s3_client, s3_test):
  file_body = 'test'
  s3 = S3Client()
  with NamedTemporaryFile(delete=True, suffix='.txt') as tmp:
    with open(tmp.name, 'w', encoding='UTF-8') as f:
      f.write(file_body)
      s3.put_object(bucket_name=BUCKET_NAME, key='files/bucket_file.txt', local_file=f.name )
    
    names = s3.list_object_names(bucket_name=BUCKET_NAME, prefix='files')
    assert names == ['files/bucket_file.txt']


def test_put_object_bucket_name_none(s3_client, s3_test):
  s3 = S3Client()
  with pytest.raises(ValueError):
    s3.put_object(bucket_name=None, key='aa', local_file='aa')


def test_put_object_key_is_none(s3_client, s3_test):
  s3 = S3Client()
  with pytest.raises(ValueError):
    s3.put_object(bucket_name='aa', key=None, local_file='aa')


def test_put_object_local_file(s3_client, s3_test):
  s3 = S3Client()
  with pytest.raises(ValueError):
    s3.put_object(bucket_name='aa', key='aa', local_file=None)
