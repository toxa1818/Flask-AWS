import unittest
from unittest.mock import MagicMock, patch
from io import BytesIO
from app import S3bucket


class TestS3bucket(unittest.TestCase):
    def setUp(self):
        self.s3bucket = S3bucket()

    def test_get_files(self):
        # Mocking S3 client
        self.s3bucket.s3.list_objects_v2 = MagicMock(return_value={'Contents': [
            {'Key': 'file1.txt', 'Size': 1024},
            {'Key': 'file2.txt', 'Size': 2048}
        ]})

        # Expected result
        expected_result = [
            {'key': 'file1.txt', 'size': 1024},
            {'key': 'file2.txt', 'size': 2048}
        ]

        # Test
        result = self.s3bucket.get_files()
        self.assertEqual(result, expected_result)

    def test_upload_file(self):
        # Mocking file object
        file = MagicMock()
        file.stream = BytesIO(b'test data')
        file.filename = 'test.txt'

        # Mocking S3 client
        self.s3bucket.s3.upload_fileobj = MagicMock()

        # Test
        self.s3bucket.upload_file(file)
        self.s3bucket.s3.upload_fileobj.assert_called_once_with(file.stream, self.s3bucket.bucket_name, file.filename)

    def test_search_files(self):
        # Mocking S3 client
        self.s3bucket.s3.list_objects_v2 = MagicMock(return_value={'Contents': [
            {'Key': 'file1.txt', 'Size': 1024},
            {'Key': 'file2.txt', 'Size': 2048}
        ]})

        # Expected result
        expected_result = [
            {'key': 'file1.txt', 'size': 1024},
            {'key': 'file2.txt', 'size': 2048}
        ]

        # Test
        result = self.s3bucket.search_files('file')
        self.assertEqual(result, expected_result)

    def test_download(self):
        # Mocking S3 resource
        s3_resource_mock = MagicMock()
        s3_resource_mock.Object.return_value.get.return_value = {
            'Body': BytesIO(b'test data')
        }
        with patch('services.s3_service.boto3') as boto_mock:
            boto_mock.resource.return_value = s3_resource_mock

            # Test
            response = self.s3bucket.download('test.txt')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b'test data')
            self.assertEqual(response.headers['Content-Disposition'], 'attachment;filename=test.txt')


if __name__ == '__main__':
    unittest.main()
