class Error(Exception):
    pass


class UniqueCredentialError(Error):
    pass


class ValueTooLargeError(Exception):
    """Raised when the input value is too large"""
    pass
