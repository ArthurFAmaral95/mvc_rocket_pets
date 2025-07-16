import pytest
from src.controllers.pet_deleter_controller import PetDeleterController

def test_delete_pet(mocker):
  mock_repository = mocker.Mock()
  controller = PetDeleterController(mock_repository)
  controller.delete('amiguinho')

  mock_repository.delete_pets.assert_called_once_with('amiguinho')

def test_delete_pet_error(mocker):
  mock_repository = mocker.Mock()
  mock_repository.delete_pets.side_effect = Exception('erro')
  controller = PetDeleterController(mock_repository)

  with pytest.raises(Exception):
    controller.delete('amiguinho')

  mock_repository.delete_pets.assert_called_once_with('amiguinho')
