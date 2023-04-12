import unittest
from unittest.mock import MagicMock
from services.ec2_service import EC2


class TestEC2(unittest.TestCase):
    def setUp(self):
        self.ec2 = EC2()
        self.instance_id = 'i-1234567890abcdef0'

    def test_create_instance(self):
        create_instances_mock = MagicMock()
        self.ec2.ec2.create_instances = create_instances_mock
        self.ec2.create_instance('test-instance', template_id='test-template-id')
        create_instances_mock.assert_called_once_with(
            LaunchTemplate={'LaunchTemplateId': 'test-template-id'},
            MaxCount=1,
            MinCount=1,
            TagSpecifications=[{'ResourceType': 'instance', 'Tags': [{'Key': 'Name', 'Value': 'test-instance'}]}]
        )

    def test_get_instances(self):
        instances_mock = MagicMock()
        instances_mock.all.return_value = []
        self.ec2.ec2.instances.all = MagicMock(return_value=instances_mock)
        expected = []
        result = self.ec2.get_instances()
        self.assertEqual(expected, result)

    def test_start_instance(self):
        instance_mock = MagicMock()
        self.ec2.ec2.Instance = MagicMock(return_value=instance_mock)
        self.ec2.start_instance(self.instance_id)
        instance_mock.start.assert_called_once()

    def test_stop_instance(self):
        instance_mock = MagicMock()
        self.ec2.ec2.Instance = MagicMock(return_value=instance_mock)
        self.ec2.stop_instance(self.instance_id)
        instance_mock.stop.assert_called_once()

    def test_reboot_instance(self):
        instance_mock = MagicMock()
        self.ec2.ec2.Instance = MagicMock(return_value=instance_mock)
        self.ec2.reboot_instance(self.instance_id)
        instance_mock.reboot.assert_called_once()

    def test_terminate_instance(self):
        instance_mock = MagicMock()
        self.ec2.ec2.Instance = MagicMock(return_value=instance_mock)
        self.ec2.terminate_instance(self.instance_id)
        instance_mock.terminate.assert_called_once()
