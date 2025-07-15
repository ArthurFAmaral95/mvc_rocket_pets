#pylint: disable=unused-argument
import pytest
from .person_finder_controller import PersonFinderController

class MockPerson:
  def __init__(self, first_name, last_name, pet_name, pet_type) -> None:
    self.first_name = first_name
    self.last_name = last_name
    self.pet_name = pet_name
    self.pet_type = pet_type

class MockPeopleRepository:
  def get_person(self, person_id: int) -> None:
    return MockPerson(
      first_name='Fulano',
      last_name='de Tal',
      pet_name='Rex',
      pet_type='fish'
    )
  
class MockPeopleRepositoryWithError:
  def get_person(self, person_id: int) -> None:
    pass

def test_find():
  person_id = 123

  mock_person_repository = MockPeopleRepository()
  controller = PersonFinderController(mock_person_repository)
  response = controller.find(person_id)

  expected_reponse = {
      'data': {
        'type': 'Person',
        'count': 1,
        'attributes': {
          'first_name': 'Fulano',
          'last_name': 'de Tal',
          'pet_name': 'Rex',
          'pet_type': 'fish'
        }
      }
    }
  
  assert response == expected_reponse

def test_find_error():
  person_id = 123

  controller = PersonFinderController(MockPeopleRepositoryWithError())
  
  with pytest.raises(Exception):
    controller.find(person_id)
