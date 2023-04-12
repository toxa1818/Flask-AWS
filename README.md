## Flask app + AWS S3
[![version](https://img.shields.io/badge/python-3.10-green)](https://semver.org)
[![version](https://img.shields.io/badge/boto3-1.26.89-green)](https://semver.org)
[![version](https://img.shields.io/badge/flask-2.2.3-green)](https://semver.org)
[![version](https://img.shields.io/badge/unittest-latest-green)](https://semver.org)

### Description:

Flask app for interacting with Amazon S3 and EC2

### Functionality:
* get all files from bucket
* upload file to bucket
* search files in bucket
* download file from bucket
* create new EC2 instance from template
* describe EC2 instances
* Actions on instances(start, stop, reboot, terminate)

![Alt text](./screens/screen_shot.png?raw=true "Optional Title")

### How to run project:
1. clone repository from github
```shell
git clone https://github.com/toxa1818/Flask-AWS.git
```
2. create s3 bucket on AWS(use management console or cli)
3. create ec2 template with needed parameters of server 
4. create IAM-user with permissions to interact with s3 and ec2
5. create file .env and write keys, bucket name, template id and your region in the following format:
```shell
KEY='YOUR ACCESS KEY ID'
SECRET_KEY='YOUR SECRET KEY'
BUCKET_NAME='YOUR BUCKET NAME'
TEMPLATE_ID='YOUR TEMPLATE ID'
REGION_NAME='YOUR REGION NAME'
```
6. install environment and dependencies
```shell
cd Flask-AWS/
python -m venv venv
source venv/bin/activate (venv/Scripts/activate for Windows)
pip install -r requirements.txt
```
7. run app
```shell
python app.py
```
8. follow the link that will appear in the terminal after starting app

### How run tests:
```shell
python -m unittest -v tests/test_s3_methods.py
python -m unittest -v tests/test_ec2_methods.py
```

### Author
Anton Andriienko
* Github: https://github.com/toxa1818
* linkedin: https://www.linkedin.com/in/anton-andriienko-62626b248/

### License
Copyright © 2023 [Anton Andriienko](https://github.com/toxa1818)
This project is [MIT](https://github.com/toxa1818/Flask-AWS/blob/main/LICENSE) licensed

