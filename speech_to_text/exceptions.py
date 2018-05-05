class APIException(Exception):
    def __init__(self, code='api_error', msg='Unexpected error'):
        super().__init__(msg)
        self.code = code
        self.msg = msg

    def to_dict(self):
        return {
            'code': self.code,
            'msg': self.msg
        }


class ExternalAPIException(APIException):
    def __init__(self, api_name='External'):
        super().__init__(
            'external_api_error',
            '{} API is not working properly}'.format(api_name)
        )


class RecognitionFailedException(APIException):
    def __init__(self):
        super().__init__(
            'recognition_failed',
            'API failed to transcript voice from your input file.'
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
