from unittest import mock
import pytest
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from sqlalchemy.orm.exc import NoResultFound
from src.models.sqlite.entities.people import PeopleTable
from .people_repository import PeopleRepository

class MockConnection:
  def __init__(self) -> None:
    self.session = UnifiedAlchemyMagicMock()

  def __enter__(self):
    return self
  
  def __exit__(self,  exc_type, exc_val, exc_tb):
    pass

class MocKConnectionNoInsertion:
  def __init__(self) -> None:
    self.session = UnifiedAlchemyMagicMock()
    self.session.add.side_effect = self.__raise_exception

  def __raise_exception(self, *args, **kwargs):
    raise Exception('No insertion made')
  
  def __enter__(self):
    return self
  
  def __exit__(self,  exc_type, exc_val, exc_tb):
    pass

class MockConnectionNoResult:
  def __init__(self) -> None:
    self.session = UnifiedAlchemyMagicMock()
    self.session.query.side_effect = self.__raise_no_result_found

  def __raise_no_result_found(self, *args, **kwargs):
    raise NoResultFound('No result found')
  
  def __enter__(self):
    return self
  
  def __exit__(self,  exc_type, exc_val, exc_tb):
    pass

def test_insert_person():
  first_name = 'first name'
  last_name = 'last name'
  age = 30
  pet_id = 2

  mock_connection = MockConnection()
  repo = PeopleRepository(mock_connection)

  repo.insert_person(first_name=first_name, last_name=last_name, age=age, pet_id=pet_id)

  mock_connection.session.add.assert_called_once()

def test_insert_person_error():
  first_name = 'first name'
  last_name = 'last name'
  age = 30
  pet_id = 2
  mock_connection = MocKConnectionNoInsertion()
  repo = PeopleRepository(mock_connection)

  with pytest.raises(Exception):
    repo.insert_person(first_name=first_name, last_name=last_name, age=age, pet_id=pet_id)
  
  mock_connection.session.rollback.assert_called_once()

def test_get_person():
  session_mock = UnifiedAlchemyMagicMock()

  query_mock = mock.MagicMock()
  query_mock.outerjoin.return_value = query_mock
  query_mock.filter.return_value = query_mock
  query_mock.with_entities.return_value = query_mock
  query_mock.one.return_value = (
    'first name',
    'last name',
    'pet name',
    'pet type'
  )

  session_mock.query.return_value = query_mock

  class MockConnectionGetPerson:
    def __init__(self):
      self.session = session_mock

    def __enter__(self):
      return self
    
    def __exit__(self,  exc_type, exc_val, exc_tb):
      pass

  mock_connection = MockConnectionGetPerson()
  repo = PeopleRepository(mock_connection)
  response = repo.get_person(1)

  mock_connection.session.query.assert_called_once_with(PeopleTable)
  assert response == ('first name', 'last name', 'pet name', 'pet type')

def test_get_person_no_result():
  mock_connection = MockConnectionNoResult()
  repo = PeopleRepository(mock_connection)

  response = repo.get_person(1)

  mock_connection.session.query.assert_called_once_with(PeopleTable)
  mock_connection.session.outerjoin.assert_not_called()
  mock_connection.session.filter.assert_not_called()
  mock_connection.session.with_entities.assert_not_called()
  mock_connection.session.one.assert_not_called()

  assert response is None
  