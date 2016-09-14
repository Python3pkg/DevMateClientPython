class DevMateError(Exception):
    """
    Base DevMate error.
    """
    pass


class IllegalArgumentError(DevMateError):
    """
    Raised if Illegal Argument passed to the function before request executed.
    """
    pass


class DevMateRequestError(DevMateError):
    """
    Base DevMate request error. Raised if request has been failed.
    Has dm_errors property with request error explanation.
    """
    dm_errors = []


class DevMateClientError(DevMateRequestError):
    """
    DevMate request error for Client errors (status code 400 - 499).
    Has dm_errors property with request error explanation.
    """
    pass


class DevMateServerError(DevMateRequestError):
    """
    DevMate request error for Server errors (status code 500 - 599).
    Has dm_errors property with request error explanation.
    """
    pass


class IncorrectParamsError(DevMateClientError):
    """
    DevMate request error for status code 400. Raised if incorrect params have been given.
    Has dm_errors property with request error explanation.
    """
    pass


class NotFoundError(DevMateClientError):
    """
    DevMate request error for status code 404. Raised if resource hasn't been found.
    Has dm_errors property with request error explanation.
    """
    pass


class ConflictError(DevMateClientError):
    """
    DevMate request error for status code 409. Raised if already existed unique param has been given.
    Has dm_errors property with request error explanation.
    """
    pass
