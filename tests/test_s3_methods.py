import unittest
from unittest.mock import MagicMock, patch
from io import BytesIO
from services.s3_service import S3bucket


class TestS3bucket(unittest.TestCase):
    def setUp(self):
        self.bucket = S3bucket()
        self.folder_path = 'my_folder'

    def test_get_files(self):
        self.bucket.s3.list_objects_v2 = MagicMock(return_value={
            'Contents': [{'Key': 'file1.txt', 'Size': 1024}],
            'CommonPrefixes': [{'Prefix': 'folder2/'}]
        })
        expected_result = [
            {'key': 'file1.txt', 'size': 1024, 'type': 'txt'},
            {'key': 'folder2', 'size': '-', 'type': 'folder'},
        ]
        result = self.bucket.get_files()
        self.assertEqual(result, expected_result)

    def test_get_files_in_folder(self):
        self.bucket.s3.list_objects_v2 = MagicMock(return_value={
            'Contents': [{'Key': 'my_folder/file2.txt', 'Size': 20}],
            'CommonPrefixes': [{'Prefix': 'my_folder/folder1/'}]
        })
        expected_files = [{'key': 'file2.txt', 'size': 20, 'type': 'txt'},
                          {'key': 'my_folder/folder1', 'size': '-', 'type': 'folder'}]

        files = self.bucket.get_files_in_folder(self.folder_path)
        self.assertEqual(files, expected_files)

    def test_create_folder(self):
        self.bucket.s3 = MagicMock()
        self.bucket.create_folder('new_folder')
        self.bucket.s3.put_object.assert_called_with(Bucket=self.bucket.bucket_name,
                                                     Key='new_folder/')
        self.bucket.create_folder('new_folder', self.folder_path)
        self.bucket.s3.put_object.assert_called_with(Bucket=self.bucket.bucket_name,
                                                     Key=f'{self.folder_path}/new_folder/')

    def test_upload_file(self):
        self.bucket.s3 = MagicMock()
        file = MagicMock()
        file.stream = BytesIO(b'test data')
        file.filename = 'test.txt'
        self.bucket.upload_file(file)
        self.bucket.s3.upload_fileobj.assert_called_with(file.stream,
                                                         self.bucket.bucket_name,
                                                         'test.txt')
        self.bucket.upload_file(file, self.folder_path)
        self.bucket.s3.upload_fileobj.assert_called_with(file.stream,
                                                         self.bucket.bucket_name,
                                                         f'{self.folder_path}/test.txt')

    def test_search_files(self):
        self.bucket.s3.list_objects_v2 = MagicMock(return_value={
            'Contents': [{'Key': 'file1.txt', 'Size': 1024}],
            'CommonPrefixes': [{'Prefix': 'folder2/'}]
        })
        expected_result = [{'key': 'file1.txt', 'size': 1024, 'type': 'txt'},
                           {'key': 'folder2', 'size': '-', 'type': 'folder'}]
        result = self.bucket.search_files('file')
        self.assertEqual(result, expected_result)

    def test_download_file(self):
        s3_resource_mock = MagicMock()
        s3_resource_mock.Object.return_value.get.return_value = {
            'Body': BytesIO(b'test data')
        }
        with patch('services.s3_service.boto3') as boto_mock:
            boto_mock.resource.return_value = s3_resource_mock
            response = self.bucket.download('test.txt')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b'test data')
            self.assertEqual(response.headers['Content-Disposition'], 'attachment;filename=None')


if __name__ == '__main__':
    unittest.main()
