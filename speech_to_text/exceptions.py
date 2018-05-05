class RecognitionFailedException(Exception):
    def __init__(self):
        super().__init__('API failed to transcript voice from your input file.')
