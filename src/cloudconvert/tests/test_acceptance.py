import os
import unittest

from mock import patch, Mock
from morelia import run

from cloudconvert import CloudConvert
from cloudconvert.sources import (InputSourceFile, InputSourceURL)


class FileConversionTests(unittest.TestCase):

    def step_I_have_created_cloudconvert_object_with_api_key(self, my_key):
        r'I have created CloudConvert instance with API key "([^"]+)"'
        self.cloudconvert = CloudConvert(api_key=my_key)

    def step_I_have_file(self, file_path):
        r'I have file "([^"]+)"'

        self._source_file = file_path

    def step_I_want_convert_it_to_pdf(self, format):
        r'I want convert it to "([^"]+)"'

        self._dest_format = format

    def step_I_run_conversion(self):
        r'I run conversion'
        ext = os.path.splitext(self._source_file)
        self.process = self.cloudconvert.convert(InputSourceFile(self._source_file, ext), self._dest_format)

    def step_I_will_get_converted_file(self):
        r'The the result will be converted file'
        result_file = self.process.download()
        assert self.process.response.get('step') == 'finished'
        assert self.process.response.get('output').get('ext') == self._dest_format
        assert self.process.response.get('output').get('url') != ''
        assert result_file != ''

    def test_file_conversion(self):
        with patch.object(InputSourceFile, 'read') as read:
            read.return_value = 'jpg content'
            with patch('cloudconvert.base.requests') as requests_base:

                process_result = Mock(status_code=200)
                process_result.json.return_value = {'url': '//localhost'}
                convertion_result = Mock(status_code=200)
                convertion_result.json.return_value = {'step': 'finished', 'output': {'ext': 'pdf', 'url': '//localhost'}}

                requests_base.post.side_effect = [process_result, convertion_result]
                requests_base.get.return_value.content = 'abc'

                filename = os.path.abspath(os.path.join(os.path.dirname(__file__), 'convert_file.feature'))
                run(filename, self)


class MergingFilesTest(unittest.TestCase):

    def setUp(self):
        self._source_files = []

    def step_I_have_created_cloudconvert_object_with_api_key(self, my_key):
        r'I have created CloudConvert instance with API key "([^"]+)"'
        self.cloudconvert = CloudConvert(api_key=my_key)

    def step_I_have_file(self, file_path):
        r'I have file "([^"]+)"'

        self._source_files.append(file_path)

    def step_I_run_merging_for_list_of_pdf_files(self):
        r'I run merging for list of PDF files'
        source_lst = []
        for file_path in self._source_files:
            ext = os.path.splitext(file_path)
            source_lst.append(InputSourceURL(file_path, ext))

        self.process = self.cloudconvert.merge(source_lst)

    def step_I_will_get_merged_file(self):
        r'I will get merged file'
        result_file = self.process.download()
        assert self.process.response.get('step') == 'finished'
        assert self.process.response.get('output').get('ext') == 'pdf'
        assert self.process.response.get('output').get('url') != ''
        assert result_file != ''

    def test_merging_files(self):
        with patch.object(InputSourceURL, 'read') as read:
            read.return_value = 'pdf content'
            with patch('cloudconvert.base.requests') as requests_base:
                process_result = Mock(status_code=200)
                process_result.json.return_value = {'url': '//localhost'}

                convertion_result = Mock(status_code=200)
                convertion_result.json.return_value = {'step': 'finished', 'ur': '//localhost', 'output': {'ext': 'pdf', 'url': '//localhost'}}

                requests_base.post.side_effect = [process_result, convertion_result]
                requests_base.get.return_value.content = 'abc'

                filename = os.path.abspath(os.path.join(os.path.dirname(__file__), 'merging_files.feature'))
                run(filename, self)
