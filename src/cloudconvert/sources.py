import os.path
import requests

from cloudconvert.exceptions import WrongResourceException


class InputSource(object):
    """Main abstract class describes input source"""

    def read(self):
        """ Reads input source file

        :returns: file object
        """
        raise NotImplemented("Method read is required")

    def get_mode(self):
        """ Returns input type mode: upload or download
        :returns: string

        """
        return self._mode

    def get_format(self):
        """ Returns input format type
        :returns: string

        """
        return self._format

    def get_filename(self):
        """ Returns name of the file
        :returns: string

        """
        raise NotImplemented("Method get_filename is required")


class InputSourceURL(InputSource):
    """Allows create input of process by URL to file and current format of the file """

    def __init__(self, url, format):
        """@todo: to be defined

        :param url: source URL to the file
        :param format: current format of the file
        """
        self._url = url
        self._format = format
        self._mode = "download"

    def read(self):
        """ Reads input source file

        :returns: file object
        """
        response = requests.get(self._url)
        if 200 < response.status_code < 201:
            raise WrongResourceException("Can read given resource")
        return response.content

    def get_filename(self):
        """
        Returns name of filename with extension
        """
        return "%s.%s" % ("", self.get_format())

    def get_url(self):
        return self._url


class InputSourceFile(InputSource):
    """Allows create input of process by path to the file or file object and current format of the file"""

    def __init__(self, file, format):
        """@todo: to be defined

        :param file: path to the file or file object
        :param format: current format of the file

        """
        self._file = file
        self._format = format
        self._mode = "upload"

    def read(self):
        """ Reads input source file

        :returns: file object
        """
        if isinstance(self._file, basestring):
            return open(self._file, 'rb')
        return self._file

    def get_filename(self):
        """
        Returns name of filename with extension
        """
        if not isinstance(self._file, basestring):
            name = "file"
        name = os.path.basename(self._file)
        return "%s.%s" % (name, self.get_format())
