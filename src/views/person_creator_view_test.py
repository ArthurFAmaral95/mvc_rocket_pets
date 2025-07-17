from typing import Dict
from .person_creator_view import PersonCreatorView
from .http_types.http_request import HttpRequest

class MockPersonCreatorController:
  def create(self, person_info: Dict) -> Dict:
    return {
     'data': {
      'type': 'Person',
      'count': 1,
      'attributes': person_info
      }
    }

def test_handle():
  http_request = HttpRequest(
    {
      'first_name': 'Fulano',
      'last_name': 'de Tal',
      'age': 30,
      'pet_id': 123
    }
  )
  view = PersonCreatorView(MockPersonCreatorController())
  response = view.handle(http_request)

  assert response.status_code == 201
  assert response.body == {'data': {'type': 'Person', 'count': 1, 'attributes': {'first_name': 'Fulano', 'last_name': 'de Tal', 'age': 30, 'pet_id': 123}}}
