"""
这个脚本用来删除JumpServer中的资产，包括用户、用户组、资产、资产节点、系统用户、资产授权、组织。
"""

import requests
import datetime
import json
from httpsig.requests_auth import HTTPSignatureAuth
from faker import Faker
from concurrent.futures import ThreadPoolExecutor
import random
import string
import time

X_JMS_ORG = "00000000-0000-0000-0000-000000000000"
GMT_FORM = '%a, %d %b %Y %H:%M:%S GMT'
headers = {
    'Accept': 'application/json',
    'X-JMS-ORG': X_JMS_ORG,
    'Date': ''
}

data = {
    'name': '',
    'username': '',
    'email': '',
    'system_roles': ["00000000-0000-0000-0000-000000000003"],
    'org_roles': ["00000000-0000-0000-0000-000000000007"],
    'source': 'openid'
}
fake = Faker()


# 获取授权
def get_auth(access_key, secret_key):
    signature_headers = ['(request-target)', 'accept', 'date']
    auth = HTTPSignatureAuth(key_id=access_key, secret=secret_key, algorithm='hmac-sha256', headers=signature_headers)
    return auth

def random_str():
    length_of_string = 8
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))

# 创建用户
def create_user(host, auth):
    headers['Date'] = datetime.datetime.utcnow().strftime(GMT_FORM)
    url = host + '/api/v1/users/users/'
    username = random_str()
    fk = Faker()
    data['name'] = username
    data['username'] = username
    data['email'] = fake.email()
    requests.post(url, auth=auth, headers=headers, data=data)


if __name__ == "__main__":
    host = "http://10.1.12.166"
    AccessKey = '5d610375-a1bc-47e9-98ac-f5ed1805138a'
    SecretKey = '5839f7b5-523c-4f84-bda9-0835195afc4a'
    auth = get_auth(AccessKey, SecretKey)
    start_time = time.time()
    print(start_time)
    futures = []
    with ThreadPoolExecutor(max_workers=13) as executor:
        for _ in range(400):
            executor.submit(create_user,host,auth)

    total_time = time.time() - start_time
    print(total_time)
