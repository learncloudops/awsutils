from typing import Any
from numbers import Number

class Validate:

  @staticmethod
  def not_null(object:Any, err_msg: str = 'the value cannot be None') -> None:
    if not object:
      raise ValueError(err_msg)


  @staticmethod
  def not_empty(object: Any, err_msg: str = 'the value cannot be None') -> None:
    Validate.not_null(object, err_msg)
    if not isinstance(object,Number) and len(object) == 0:
      raise ValueError(err_msg)