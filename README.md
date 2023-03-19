## Flask app + AWS S3
[![version](https://img.shields.io/badge/python-3.10-green)](https://semver.org)
[![version](https://img.shields.io/badge/boto3-1.26.89-green)](https://semver.org)
[![version](https://img.shields.io/badge/flask-2.2.3-green)](https://semver.org)
[![version](https://img.shields.io/badge/unittest-latest-green)](https://semver.org)

### Description:

Flask app for interacting with Amazon S3 bucket

### Functionality:
* get all files from bucket
* upload file to bucket
* search files in bucket
* download file from bucket

![Alt text](./screens/example.png?raw=true "Optional Title")

### How to run project:
1. clone repository from github
```shell
git clone https://github.com/toxa1818/Flask-AWS.git
```
2. install environment and dependencies
```shell
cd Flask-AWS/
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3. run app
```shell
python app.py
```
4. follow the link that will appear in the terminal after starting app

### How run tests:
```shell
python -m unittest -v tests/test_s3_methods.py
```

### Author
Anton Andriienko
* Github: https://github.com/toxa1818
* linkedin: https://www.linkedin.com/in/anton-andriienko-62626b248/

### License
Copyright © 2023 [Anton Andriienko](https://github.com/toxa1818)
This project is [MIT](https://github.com/toxa1818/Flask-AWS/blob/main/LICENSE) licensed

