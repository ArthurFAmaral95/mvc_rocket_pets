from unittest import mock
import pytest
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from src.models.sqlite.entities.pets import PetsTable
from .pets_repository import PetsRepository
from .people_repository_test import MockConnectionNoResult

class MockConnection:
  def __init__(self) -> None:
    self.session = UnifiedAlchemyMagicMock(
      data=[
        (
          [mock.call.query(PetsTable)], #quando eu fizer uma query
          [
            PetsTable(name='dog', type='dog'),
            PetsTable(name='cat', type='cat')
          ] #vou ter um resultado
        )
      ]
    )
    
  def __enter__(self):
    return self
  
  def __exit__(self, exc_type, exc_val, exc_tb):
    pass

def test_list_pets():
  mock_connection = MockConnection()
  repo = PetsRepository(mock_connection)
  response = repo.list_pets()

  mock_connection.session.query.assert_called_once_with(PetsTable)
  mock_connection.session.all.assert_called_once()
  mock_connection.session.filter.assert_not_called()

  assert response[0].name == 'dog'
  assert response[0].type == 'dog'
  assert response[1].name == 'cat'
  assert response[1].type == 'cat'

def test_delete_pet():
  mock_connection = MockConnection()
  repo = PetsRepository(mock_connection)

  repo.delete_pets('petName')

  mock_connection.session.query.assert_called_once_with(PetsTable)
  mock_connection.session.filter.assert_called_once_with(PetsTable.name == 'petName')
  mock_connection.session.delete.assert_called_once()

def test_list_pets_no_result():
  mock_connection = MockConnectionNoResult()
  repo = PetsRepository(mock_connection)
  response = repo.list_pets()

  mock_connection.session.query.assert_called_once_with(PetsTable)
  mock_connection.session.all.assert_not_called()
  mock_connection.session.filter.assert_not_called()

  assert response is None

def test_delete_pet_error():
  mock_connection = MockConnectionNoResult()
  repo = PetsRepository(mock_connection)

  with pytest.raises(Exception):
    repo.delete_pets('petName')

  mock_connection.session.rollback.assert_called_once()
