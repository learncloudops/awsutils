import pytest
from awsutils.services import Validate

def test_str_not_null_success():
  Validate.not_null(object='test', err_msg='the value is null')


def test_str_not_null_failure():
  with pytest.raises(ValueError):
    Validate.not_null(object=None, err_msg='the value is null')


def test_str_not_null_err_msg():
  err = 'the error is customizable'
  try:
    Validate.not_null(object=None, err_msg=err )
    pytest.fail()
  except ValueError as ve:
    assert str(ve) == err


def test_obj_not_null_success():
  obj = { 'foo': 'bar'}
  Validate.not_null(object=obj, err_msg='the value is null')


def test_str_not_empty_success():
  Validate.not_empty(object='ok', err_msg='everything should be ok')


def test_str_not_empty_fails_when_null():
  try:
    Validate.not_empty(object=None, err_msg='custom error message')
    pytest.fail()
  except ValueError as e:
    assert 'custom error message' == str(e)


def test_str_not_empty_fails_when_empty():
  try:
    Validate.not_empty(object='', err_msg='custom error message')
    pytest.fail()
  except ValueError as e:
    assert 'custom error message' == str(e)


def test_str_not_empty_fails_when_space():
  try:
    Validate.not_empty(object=' ', err_msg='custom error message')
    pytest.fail()
  except ValueError as e:
    assert 'custom error message' == str(e)
