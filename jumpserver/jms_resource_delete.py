"""
这个脚本用来删除JumpServer中的资产，包括用户、用户组、资产、资产节点、系统用户、资产授权、组织。
"""

import requests
import datetime
import json
import time
from httpsig.requests_auth import HTTPSignatureAuth
from concurrent.futures import ThreadPoolExecutor

X_JMS_ORG = "00000000-0000-0000-0000-000000000000"
GMT_FORM = '%a, %d %b %Y %H:%M:%S GMT'
headers = {
    'Accept': 'application/json',
    'X-JMS-ORG': X_JMS_ORG,
    'Date': ''
}


# 获取授权
def get_auth(access_key, secret_key):
    signature_headers = ['(request-target)', 'accept', 'date']
    auth = HTTPSignatureAuth(key_id=access_key, secret=secret_key, algorithm='hmac-sha256', headers=signature_headers)
    return auth


# 获取组织信息
def get_org_info(host, auth):
    url = host + '/api/v1/orgs/orgs/'
    headers['Date'] = datetime.datetime.utcnow().strftime(GMT_FORM)
    response = requests.get(url, auth=auth, headers=headers, timeout=120)
    orgs = json.loads(response.text)
    org_ids = []
    for org in orgs:
        if org["name"] != "Default":
            org_ids.append(org["id"])
    # print(org_ids)
    return org_ids


# 获取用户信息
def get_user_info(host, auth):
    url = host + '/api/v1/users/users/'
    headers['Date'] = datetime.datetime.utcnow().strftime(GMT_FORM)
    response = requests.get(url, auth=auth, headers=headers, timeout=120)
    users = json.loads(response.text)
    # print(users)
    user_ids = []
    for user in users:
        if user["username"] != "admin":
            user_ids.append(user["id"])
    return user_ids


# 获取用户组信息
def get_groups_info(host, auth):
    url = host + '/api/v1/users/groups/'
    headers['Date'] = datetime.datetime.utcnow().strftime(GMT_FORM)
    response = requests.get(url, auth=auth, headers=headers, timeout=120)
    groups = json.loads(response.text)
    group_ids = []
    for group in groups:
        group_ids.append(group["id"])
    return group_ids


# 获取资产信息
def get_assets_info(host, auth):
    url = host + '/api/v1/assets/assets/'
    headers['Date'] = datetime.datetime.utcnow().strftime(GMT_FORM)
    response = requests.get(url, auth=auth, headers=headers)
    assets = json.loads(response.text)
    asset_ids = []
    for asset in assets:
        asset_ids.append(asset["id"])
    # print(asset_ids)
    return asset_ids


# 获取资产节点信息
def get_assets_node_info(host, auth):
    url = host + '/api/v1/assets/nodes/'
    headers['Date'] = datetime.datetime.utcnow().strftime(GMT_FORM)
    response = requests.get(url, auth=auth, headers=headers, timeout=120)
    system_users = json.loads(response.text)
    system_user_ids = []
    for system_user in system_users:
        system_user_ids.append(system_user["id"])
    return system_user_ids


# 获取系统用户
def get_assets_system_users(host, auth):
    url = host + '/api/v1/assets/system-users/'
    headers['Date'] = datetime.datetime.utcnow().strftime(GMT_FORM)
    response = requests.get(url, auth=auth, headers=headers, timeout=240)
    nodes = json.loads(response.text)
    node_ids = []
    for node in nodes:
        try:
            int(node["key"])
        except:
            node_ids.append(node["id"])
    return node_ids


# 获取资产授权
def get_assets_permissions(host, auth, asset_id=None):
    if asset_id == None:
        url = host + '/api/v1/perms/asset-permissions/'
    else:
        url = host + '/api/v1/perms/asset-permissions/' + '?asset_id=' + asset_id
    headers['Date'] = datetime.datetime.utcnow().strftime(GMT_FORM)
    response = requests.get(url, auth=auth, headers=headers, timeout=1200)
    # print(response.text)
    permissions = json.loads(response.text)
    permission_ids = []
    for permission in permissions:
       permission_ids.append(permission["id"])
    return permission_ids


# 删除用户
def delete_user(host, auth, user_id):
    headers['Date'] = datetime.datetime.utcnow().strftime(GMT_FORM)
    url = host + '/api/v1/users/users/' + user_id + '/'
    requests.delete(url, auth=auth, headers=headers)


# 删除用户组
def delete_group(host, auth, group_id):
    GMT_FORM = '%a, %d %b %Y %H:%M:%S GMT'
    headers['Date'] = datetime.datetime.utcnow().strftime(GMT_FORM)
    url = host + '/api/v1/users/groups/' + group_id + '/'
    requests.delete(url, auth=auth, headers=headers)


# 删除资产
def delete_asset(host, auth, asset_id):
    url = host + '/api/v1/assets/assets/' + asset_id + '/'
    headers['Date'] = datetime.datetime.utcnow().strftime(GMT_FORM)
    requests.delete(url, auth=auth, headers=headers)


# 删除资产节点
def delete_assets_node(host, auth, node_id):
    url = host + '/api/v1/assets/nodes/' + node_id + '/'
    headers['Date'] = datetime.datetime.utcnow().strftime(GMT_FORM)
    requests.delete(url, auth=auth, headers=headers)


# 删除系统用户
def delete_assets_system_user(host, auth, system_user_id):
    headers['Date'] = datetime.datetime.utcnow().strftime(GMT_FORM)
    url = host + '/api/v1/assets/system-users/' + system_user_id + '/'
    requests.delete(url, auth=auth, headers=headers)


# 删除资产授权
def delete_assets_permission(host, auth, permission_id):
    headers['Date'] = datetime.datetime.utcnow().strftime(GMT_FORM)
    url = host + '/api/v1/perms/asset-permissions/' + permission_id + '/'
    requests.delete(url, auth=auth, headers=headers)


# 删除组织
def delete_org(host, auth, org_id):
    headers['Date'] = datetime.datetime.utcnow().strftime(GMT_FORM)
    url = host + '/api/v1/orgs/orgs/' + org_id + '/'
    requests.delete(url, auth=auth, headers=headers)


# 删除所有资源
def delete_all(host, auth, workers=None):
    if workers is None:
        workers = 10
    with ThreadPoolExecutor(max_workers=workers) as executor:
        # 删除用户
        user_ids = get_user_info(host, auth)
        if user_ids:
            for user_id in user_ids:
                executor.submit(delete_user, host, auth, user_id)
        # 删除用户组
        group_ids = get_groups_info(host, auth)
        if group_ids:
            for group_id in group_ids:
                executor.submit(delete_group, host, auth, group_id)

        # 删除资产
        asset_ids = get_assets_info(host, auth)
        if asset_ids:
            for asset_id in asset_ids:
                executor.submit(delete_asset, host, auth, asset_id)

        # 删除系统用户
        system_user_ids = get_assets_system_users(host, auth)
        if system_user_ids:
            for system_user_id in system_user_ids:
                executor.submit(delete_assets_system_user, host, auth, system_user_id)
        # 删除授权
        permission_ids = get_assets_permissions(host, auth)
        if permission_ids:
            for permission_id in permission_ids:
                executor.submit(delete_assets_permission, host, auth, permission_id)

        # 删除资产节点
        node_ids = get_assets_node_info(host, auth)
        if node_ids:
            for node_id in node_ids:
                executor.submit(delete_assets_node, host, auth, node_id)

        # 删除组织
        org_ids = get_org_info(host, auth)
        if org_ids:
            for org_id in org_ids:
                executor.submit(delete_org, host, auth, org_id)


if __name__ == "__main__":
    host = "http://10.1.12.166"
    AccessKey = '172e3f6c-192a-46c2-aa7c-11919d784e43'
    SecretKey = '39deb43f-3500-40e0-9f5d-e15788419f9e'
    # host = "http://democenter.fit2cloud.com:10888/"
    # AccessKey = '5911c540-d6ee-4990-ada0-b2ef9e6a6c78'
    # SecretKey = '698b19a0-74ef-4d18-814c-8c2a0e9a2794'
    auth = get_auth(AccessKey, SecretKey)
    delete_all(host, auth)
    # get_user_info(host, auth)
    # start_time = time.time()
    # get_assets_permissions(host, auth, asset_id="4c801e93-2a4c-45c3-8413-b9cf902e8413")
    # total_time = time.time() - start_time
    # print(total_time)
