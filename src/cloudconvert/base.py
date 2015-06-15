import json
import requests

from cloudconvert.exceptions import (
    MissingFileException, WrongRequestDataException, FilesCountException)

CLOUD_CONVERT_PROCESS_URL = 'http://api.cloudconvert.com/process'
CONVERSION_PROCESS = 'convert'
MERGING_PROCESS = 'merge'
MAX_FILES_COUNT = 10


class Process(object):
    """Main process class """

    def __init__(self, cloudconvert, url, output_format):
        """Constructor of Process class

        :param cloudconvert: CloudConvert parent object
        :param url: process url
        :param output_format: output file format

        """
        self._cloudconvert = cloudconvert
        self._output_format = output_format
        self._url = url
        self.files = []

    def _get_file_data(self, file_name):
        return open(file_name, 'rb')

    def _get_processed_file_url(self):
        """ Preparse url to processed file

        :returns: empty string or url to file
        """
        url = self.response.get('url', '')
        return 'http:%s' % url if url else ''

    def add_file(self, source):
        """ Assigns file source into process files list

        :param file: InputSource
        """
        self.files.append(source)

    def start_process(self):
        """ Processes files and saves json on response attribute
        """
        response = self._make_process_request()
        self.response = response

    def download(self):
        """ Downloads processed file

        :returns: binary file
        """
        url = self._get_processed_file_url()
        result = requests.get(url)
        return result.content


class ConversionProcess(Process):
    """ Supports converion methods """

    def _get_files(self):
        """Prepares list of dict in format
        [
            {'filename': filename, 'file': binary_file_data},
        ]
        :returns: empty list or list of dicts
        """
        files = []
        for source in self.files:
            files.append(('file', (source.get_filename(), source.read())))
        return files

    def get_mode(self):
        """ Returns source input type: upload or download
        :returns: string

        """
        return self.files[0].get_mode()

    def _make_process_request(self):
        """@todo: Docstring for _make_convert_request
        :returns: json or MissingFileException
        """
        mode = self.get_mode()
        files = self._get_files()
        if not files:
            raise MissingFileException('Missing file')

        data = {
            'input': mode,
            'wait': True,
            'outputformat': self._output_format
        }

        response = requests.post(self._url, data=data, files=files)

        if response.status_code not in (200, 201):
            raise WrongRequestDataException(response.content)
        return response.json()


class MergingProcess(Process):
    """ Supports merging methods """

    def _get_files(self):
        files = []
        for index, source in enumerate(self.files):
            files.append({"file": source.get_url(), "filename": '%s.pdf' % index})
        return files

    def _make_process_request(self):
        """@todo: Docstring for _make_convert_request
        :returns: json or MissingFileException
        """
        files = self._get_files()
        if not files:
            raise MissingFileException('Missing file')

        data = {
            'input': 'download',
            'wait': True,
            'outputformat': self._output_format,
            'filename': 'merged.pdf',
            'file': files
        }

        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.post(self._url, data=json.dumps(data), headers=headers)

        if response.status_code not in (200, 201):
            raise WrongRequestDataException(response.content)
        return response.json()

PROCESS_BUILDER = {
    CONVERSION_PROCESS: ConversionProcess,
    MERGING_PROCESS: MergingProcess
}


class CloudConvert(object):
    """Docstring for CloudConvert """

    def __init__(self, api_key, process_builder=None):
        """@todo: to be defined

        :param api_key: @todo

        """
        if process_builder is None:
            process_builder = PROCESS_BUILDER
        self._process_builder = process_builder
        self._api_key = api_key

    def _get_data(self, input_format, output_format):
        """ Prepares
        """
        return json.dumps({
            'inputformat': input_format,
            'outputformat': output_format
        })

    def _get_headers(self):
        """ Prepares authentication headers

        :returns: dict of HTTP headers
        """
        return {
            'Content-Type': 'multipart/form-data',
            'Authorization': 'Bearer {}'.format(self._api_key)}

    def _get_process_url(self, input_format, output_format):
        """@todo: Docstring for _get_process_url
        :param input_format: @todo
        :param output_format: @todo
        :returns: @todo

        """
        data = self._get_data(input_format, output_format)
        headers = self._get_headers()

        response = requests.post(CLOUD_CONVERT_PROCESS_URL, data=data, headers=headers)
        if response.status_code != 200:
            raise WrongRequestDataException('Wrong request for process: %s' % response.content)

        response_data = response.json()
        return response_data.get('url')

    def _create_process(self, input_format, output_format, process_type):
        """ Creates process for conversion or merging file

        :param input_format: input file format e.g. jpg
        :param output_format: output file format e.g. pdf
        :returns: new ConversionProcess or MergingProcess object

        """
        url = 'http:%s' % self._get_process_url(input_format, output_format)
        return self._process_builder[process_type](self, url, output_format)

    def convert(self, source, output_format):
        """ Converts file from input format to output_format

        :param source: InputSource object
        :param output_format: output format file e.g. pdf
        returns: Process object

        """
        self.process = self._create_process(source.get_format(), output_format, CONVERSION_PROCESS)
        self.process.add_file(source)
        self.process.start_process()
        return self.process

    def merge(self, files):
        """ Merge PDF files into one PDF file

        :param files: list of InputSourceURL objects e.g. [InputSourceURL('http://localhost/abc.pdf'), ]
        returns: Process object

        """
        if len(files) > MAX_FILES_COUNT:
            raise FilesCountException('Too many files to merge in one process')
        self.process = self._create_process('pdf', 'pdf', MERGING_PROCESS)
        for source in files:
            self.process.add_file(source)
        self.process.start_process()
        return self.process
