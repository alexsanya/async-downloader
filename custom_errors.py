class InputError(Exception):
    """Exception raised for errors in the input.

    Attributes:
      expression -- input expression in which the error occurred
      message -- explanation of the error
    """

    def __init__(self, expression, message):
        Exception.__init__(self)
        self.expression = expression
        self.message = message
