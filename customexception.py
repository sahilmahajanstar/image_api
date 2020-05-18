# Inherit exception class to generate our own exception
class Imageapi(Exception):
    ''' Base class for exception'''
    pass
class ApiLimitExceed(Imageapi):
    def __init__(self):
        self.message='Limit Exceed Api Rate is 5 request/minute'
    