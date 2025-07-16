from src.models.sqlite.entities.pets import PetsTable
from .pet_lister_controller import PetListerController

class MockPetRepository:
  def list_pets(self):
    return [
      PetsTable(name='Rex', type='fish', id=1),
      PetsTable(name='Dog', type='cat', id=2)
    ]
  
class MockPetRepositoryError:
  def list_pets(self):
    return []

def test_list_pets():
  controller = PetListerController(MockPetRepository())
  response = controller.list()

  expected_response = {
      'data': {
        'type': "Pets",
        'count': 2,
        'attributes': [
          {'name': 'Rex', 'type': 'fish', 'id': 1},
          {'name': 'Dog', 'type': 'cat', 'id': 2},
        ]
      }
    }
  
  assert response == expected_response

def test_list_pets_error():
  controller = PetListerController(MockPetRepositoryError())
  response = controller.list()

  expected_response = {
      'data': {
        'type': "Pets",
        'count': 0,
        'attributes': []
      }
    }
  assert response == expected_response
