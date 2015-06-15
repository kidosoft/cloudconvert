from cloudconvert import CloudConvert
from cloudconvert.base import ConversionProcess
from cloudconvert.sources import InputSourceFile

from mock import Mock, patch
from unittest import TestCase


class CloudConvertConvertTest(TestCase):

    @patch('cloudconvert.base.requests')
    def test_should_create_convert_process(self, requests):
        # Arrange
        cc = CloudConvert(api_key='123')
        source = Mock(InputSourceFile)
        source.get_format.return_value = 'jpg'
        dest_format = 'pdf'
        response = requests.post.return_value
        response.status_code = 200
        response.json.return_value = {'url': 'abc'}
        # Act
        result = cc.convert(source, dest_format)
        # Assert
        self.assertTrue(isinstance(result, ConversionProcess))
