from typing import Dict
from .pet_lister_view import PetListerView
from .http_types.http_request import HttpRequest

class MockPetListerController:
  def list(self) -> Dict:
    return {
      'data': {
      'type': "Pets",
      'count': 1,
      'attributes': [{'name': 'Rex', 'type': 'fish', 'id': 1}]
     }
    }
  
def test_handle():
  http_request = HttpRequest()
  view = PetListerView(MockPetListerController())
  response = view.handle(http_request)

  assert response.status_code == 200
  assert response.body == {'data': {'type': 'Pets', 'count': 1, 'attributes': [{'name': 'Rex', 'type': 'fish', 'id': 1}]}}
