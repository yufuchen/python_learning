import requests
import json
import random
import string
from jumpserver.datas_generator import MySQLConnector
from faker import Faker

db_server = '10.1.12.203'
db_user = 'root'
db_passwd = 'Password123@mysql'

server_host = "http://10.1.12.203"
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Content-Type": "application/json;charset=UTF-8",
    "Cookie": "KEYCLOAK_LOCALE=zh-CN; FIT2CLOUD_SESSION_ID=node0jrvoinyd15mb10rll82ljzkyk8.node0; JSESSIONID=node01jmyi7ynb66cbk42r0q6jtvbg20.node0",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.71",
}

payload = {"id": "%test%"}
s = requests.session()

db = MySQLConnector(db_server, db_user, db_passwd, "fit2cloud")


def random_str():
    length_of_string = 8
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))


def add_org(pid):
    payload = {
        "description": None,
        "name": random_str(),
        "pid": pid
    }
    path = "/management-center/organization/add"
    rsp = s.post(server_host + path, data=json.dumps(payload), headers=headers)


# print(rsp.text)s


def add_workspaces(organizationId):
    payload = {
        "description": None,
        "name": random_str(),
        "organizationId": organizationId
    }
    path = "/management-center/workspace/add"
    s.post(server_host + path, data=json.dumps(payload), headers=headers)


def add_roles(workspaceIds, userIdList):
    payload = {
        "roleInfoList": [
            {
                "organizationIds": [],
                "roleId": "USER",
                "selectOrganizationId": "",
                "workspace": True,
                "workspaceIds": workspaceIds
            }
        ],
        "userIdList": userIdList
    }
    path = "/management-center/user/role/add"
    s.post(server_host + path, data=json.dumps(payload), headers=headers)

def server_grant(cloud_server_id, workspace_id):
    payload = cloud_server_id
    path = "/vm-service/server/grant/" + workspace_id
    s.post(server_host + path, data=json.dumps(payload), headers=headers)
    # print(rsp.text)

def get_orgs():
    payload = {}
    path = "/management-center/organization/1/1000"
    rsp = s.post(server_host + path, data=json.dumps(payload), headers=headers)
    # print(rsp.text)
    orgs = json.loads(rsp.text)["data"]["listObject"]
    return orgs


if __name__ == "__main__":
    # for i in range(10):
    #     add_org(None)
    # 创建多级组织
    # orgs = get_orgs()
    # print(orgs)
    # for org in orgs:
    #     if org["level"] == 1:
    #         pid = org["id"]
    #         for _ in range(3):
    #             add_org(pid)

    # 创建工作空间
    # db.cursor.execute("select id from organization;")
    # orgs = db.cursor.fetchall()
    #
    # for org in orgs:
    #     organizationId = org[0]
    #     # print(organizationId)
    #     add_workspaces(organizationId)

    # 为用户添加工作空间角色
    # db.cursor.execute("select id from workspace;")
    # workspaces = db.cursor.fetchall()
    # db.cursor.execute("SELECT id from `user`where id != 'admin';")
    #
    # for wrokspace in workspaces:
    #     workspaceIds = list(wrokspace)
    #     userIdList = list(db.cursor.fetchone())
    #     print(workspaceIds, userIdList)
    #     add_roles(workspaceIds, userIdList)

    # 虚拟机授权到工作空间
    db.cursor.execute("select id from workspace;")
    workspaces = db.cursor.fetchall()
    db.cursor.execute("SELECT id  from cloud_server;")
    for workspace in workspaces:
        workspace_id = workspace[0]
        cloud_server_id = list(db.cursor.fetchone())
        server_grant(cloud_server_id, workspace_id)
