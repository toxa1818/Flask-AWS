from flask import Blueprint, render_template, request, redirect, url_for
from services.ec2_service import EC2
import logging
from logging.config import fileConfig


ec2_routes = Blueprint('ec2_routes', __name__)
client = EC2()
logging.config.fileConfig(fname='logs/logging.conf')
logger = logging.getLogger('app')


@ec2_routes.route('/ec2_service')
def get_instances():
    try:
        instances = client.get_instances()
        logger.info('Get all EC2 Instances')
        return render_template('ec2_service.html', instances=instances)
    except Exception as e:
        logger.error(f'Error in getting instances: {str(e)}')
        raise


@ec2_routes.route('/ec2_service/create_instance', methods=['POST'])
def create_instance():
    try:
        instance_name = request.form['instance_name']
        client.create_instance(instance_name)
        logger.info(f'EC2 Instance {instance_name} was created')
        return redirect('/ec2_service')
    except Exception as e:
        logger.error(f'Error in creating instance: {str(e)}')
        raise


@ec2_routes.route('/ec2_service/instance_action')
def instance_action():
    try:
        action = request.args.get('action')
        instance_id = request.args.get('instance_id')
        if action == 'start':
            client.start_instance(instance_id)
        elif action == 'stop':
            client.stop_instance(instance_id)
        elif action == 'reboot':
            client.reboot_instance(instance_id)
        elif action == 'terminate':
            client.terminate_instance(instance_id)
        logger.info(f'Action {action} of instance was completed')
        return redirect('/ec2_service')
    except Exception as e:
        logger.error(f'Error in execution of action {action} of instance: {str(e)}')
        raise


# @ec2_routes.route('/ec2_service/connect_to_instance/<string:instance_id>')
# def connect_to_instance(instance_id):
#     try:
#         session_id, target_instance_id = client.connect_to_instance(instance_id)
#         logger.info(f'Connecting to instance {instance_id} was successful')
#         return render_template('connect.html', session_id=session_id, target_instance_id=target_instance_id)
#     except Exception as e:
#         logger.error(f'Error in connecting to instance: {str(e)}')
#         raise
