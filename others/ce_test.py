import requests
import json
host = "http://democenter.fit2cloud.com:22222"
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Content-Type": "application/json;charset=UTF-8",
    "Cookie": "KEYCLOAK_LOCALE=zh-CN; FIT2CLOUD_SESSION_ID=node013g5njx9j047e11d76fbe64q082757.node0; JSESSIONID=node01e16wr86fxbii5dyvluezel5d39.node0",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.76",
}
path = "/management-center/user/1/1000"
payload = {"id": "%test%"}
s = requests.session()
rsp = s.post(host + path, data=json.dumps(payload), headers=headers)
# print(rsp.text)
users = json.loads(rsp.text)["data"]["listObject"]
print(users)
for user in users:
    print(user["id"])
    s.post(host + "/management-center/user/delete/" + user["id"], headers=headers)