import pytest
import os
import boto3
from moto import mock_s3, mock_events


@pytest.fixture
def aws_credentials():
  os.environ["AWS_ACCESS_KEY_ID"] = "testing"
  os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
  os.environ["AWS_SECURITY_TOKEN"] = "testing"
  os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture
def s3_client(aws_credentials):
  with mock_s3():
    conn = boto3.client('s3', region_name='us-east-1')
    yield conn


@pytest.fixture
def events_client(aws_credentials):
  with mock_events():
    conn = boto3.client('events', region_name='us-east-1')
    yield conn