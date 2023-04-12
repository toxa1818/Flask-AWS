import boto3
import os
from dotenv import load_dotenv


load_dotenv()


class EC2:
    def __init__(self):
        self.ec2 = boto3.resource('ec2',
                                  aws_access_key_id=os.environ.get('KEY'),
                                  aws_secret_access_key=os.environ.get('SECRET_KEY'),
                                  region_name=os.environ.get('REGION_NAME'))

    def get_instances(self):
        result = []
        instances = self.ec2.instances.all()
        for instance in instances:
            result.append(instance)
        return result

    def create_instance(self, instance_name, template_id=os.environ.get('TEMPLATE_ID')):
        launch_template = {'LaunchTemplateId': template_id}
        self.ec2.create_instances(LaunchTemplate=launch_template,
                                  MaxCount=1,
                                  MinCount=1,
                                  TagSpecifications=[{'ResourceType': 'instance',
                                                      'Tags': [{'Key': 'Name', 'Value': instance_name}]
                                                      }])

    def start_instance(self, instance_id):
        instance = self.ec2.Instance(instance_id)
        instance.start()

    def stop_instance(self, instance_id):
        instance = self.ec2.Instance(instance_id)
        instance.stop()

    def reboot_instance(self, instance_id):
        instance = self.ec2.Instance(instance_id)
        instance.reboot()

    def terminate_instance(self, instance_id):
        instance = self.ec2.Instance(instance_id)
        instance.terminate()

    def connect_to_instance(self, instance_id):
        pass
