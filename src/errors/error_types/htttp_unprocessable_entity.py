class HttpUnprocessableEntityError(Exception):
  def __init__(self, message):
    super().__init__(message)
    self.status_code = 422
    self.name = 'UnprocessableEntity'
    self.message = message
