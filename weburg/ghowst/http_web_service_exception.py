class HttpWebServiceException(RuntimeError):
    http_status = 0
    message = ''

    def __init__(self, http_status, message):
        super()
        self.http_status = http_status
        self.message = message
