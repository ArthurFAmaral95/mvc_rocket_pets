from .pet_deleter_view import PetDeleterView
from .http_types.http_request import HttpRequest

class MockPetDeleterController:
  def delete(self, name: str) -> None:
    pass

def test_handle():
  http_request = HttpRequest(param={'name': 'Rex'})
  view = PetDeleterView(MockPetDeleterController())
  response = view.handle(http_request)

  assert response.status_code == 204
