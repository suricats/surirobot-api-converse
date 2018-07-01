class APIException(Exception):
    def __init__(self, code='api_error', msg='Unexpected error'):
        super().__init__(msg)
        self.code = code
        self.msg = msg

    def __str__(self):
        if self.code is None:
            self.code = 'unknown-error'
        if self.msg is None:
            self.msg = '{}: Unexpected error.\nCode: {}'.format(type(self).__name__, self.code)
        return self.msg

    def __iter__(self):
        yield 'code', self.code
        yield 'msg', self.msg


class ExternalAPIException(APIException):
    def __init__(self, api_name='External'):
        super().__init__(
            'external_api_error',
            '{} API is not working properly'.format(api_name)
        )


class InvalidCredentialsException(APIException):
    def __init__(self, api_name='External'):
        super().__init__(
            'invalid_credentials_error',
            '{} API credentials are not valid.'.format(api_name)
        )


class OperationFailedException(APIException):
    def __init__(self):
        super().__init__(
            'operation_failed',
            'API failed to process your request. Try again.'
        )


class MissingParameterException(APIException):
    def __init__(self, parameter):
        super().__init__(
            'missing_parameter',
            '{} is missing.'.format(parameter)
        )


class BadParameterException(APIException):
    def __init__(self, parameter, valid_values=None):
        msg = '{} is not correct.'.format(parameter)
        if valid_values:
            msg = msg + ' Valid values are {}'.format(', '.join(valid_values))
        super().__init__(
            'bad_parameter',
            msg
        )
