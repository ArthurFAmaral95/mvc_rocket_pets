class HttpBadRequestError(Exception):
  def __init__(self, message):
    super().__init__(message)
    self.status_code = 400
    self.name = 'BadRequest'
    self.message = message
