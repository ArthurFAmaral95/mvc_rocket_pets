from .person_finder_view import PersonFinderView
from .http_types.http_request import HttpRequest

class MockPersonFinderController:
  def find(self, _person_id: int) -> None:
    return {
      'data': {
       'type': 'Person_test',
       'count': 1,
       'attributes': {
         'first_name': 'Fulano',
         'last_name': 'de Tal',
         'pet_name': 'Rex',
         'pet_type': 'Fish'
       }
     }
    }
  
def test_handle():
  http_request = HttpRequest(param={'person_id': 1})
  view = PersonFinderView(MockPersonFinderController())
  response = view.handle(http_request)

  assert response.status_code == 200
  assert response.body == {'data': {'type': 'Person_test', 'count': 1, 'attributes': {'first_name': 'Fulano', 'last_name': 'de Tal', 'pet_name': 'Rex', 'pet_type': 'Fish'}}}
