"""
CloudConvert exceptions classes.
"""


class CloudConvertError(Exception):
    """ Basic CloudConvert exceptions class. """
    pass


class MissingFileException(CloudConvertError):
    """Raises when file to conversion is missed. """
    pass


class WrongRequestDataException(CloudConvertError):
    """Raises when some data in request sending to cloudconvert service are missed. """
    pass


class WrongResourceException(CloudConvertError):
    """Raises when given resource URL is wrong. """
    pass


class FilesCountException(CloudConvertError):
    """Raises when too many files are sent in one request """
