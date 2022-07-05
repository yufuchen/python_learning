import requests
import json
import csv
base_url  = "http://139.224.45.86"
headers = {
    "Accept":"application/json, text/plain, */*",
    "Content-Type": "application/json"
}
username = "EJ8K8qQihJJg+aM/d9U/EWM4hr8NMv+qmU1keKE4aNImCJn+EFN2+g9kOSgi9x2KgTlot1ZXQbMtcAIgDmgyQQ=="
password = "zZ9kuBgxppHHbUAESXQxIxdPm+B8tWEL3HHn6LQLUHVN6AlUz0Fglg/OSkn4Er/b00W1WpP/fxtJFIi6Y4vF0Q=="
data = {
    "username": username,
    "password": password,
    "loginType": 0
}

login_path = "/api/auth/login"
s = requests.Session()
# 登录
def login():
    rsp = s.post(base_url+login_path,data=json.dumps(data),headers=headers)
    j = json.loads(rsp.text)
    print(j["data"]["token"])
    headers["Authorization"] = j["data"]["token"]

# 获取数据集组
def dataset_group():
    rsp = s.post(base_url + "/authModel/queryAuthModel", data=json.dumps({"modelType": "dataset"}), headers=headers)
    return json.loads(rsp.text)["data"]

# 获取数据源
def get_datasource_list():
    rsp = s.get(base_url+"/datasource/list",  headers=headers)
    return json.loads(rsp.text)["data"]

# 创建数据集
def creat_dataset():
    datasources = get_datasource_list()
    scene_id = dataset_group()[5]["id"]
    for datasource in datasources:
        datasource_id = datasource["id"]
        datasource_name = datasource["name"]
        if datasource_name not in ["demo", "dataease_dataset_zhilian"]:

            data = [{
            "name": datasource_name + "_bills_item_price_big_data2",
            "sceneId": scene_id,
            "dataSourceId": datasource_id,
            "type": "db",
            "syncType": "sync_latter",
            "mode": 1,
            "info": "{\"table\":\"bills_item_price_big_data2\"}"
            }]
            rsp = s.post(base_url+"/dataset/table/batchAdd", data=json.dumps(data), headers=headers)
            print(rsp.text)
            # print(data)

# 创建数据集同步任务
def create_dataset_rask():
    dataset_ids = dataset_group()[5]['children']
    for dataset_id in dataset_ids:
        data = {
            "datasetTableTask": {
                "name": "rask_5000",
                "type": "all_scope",
                "startTime": 1642572453006,
                "rate": "SIMPLE_CRON",
                "endTime": 0,
                "end": 1652582453006,
                "extraData": "{\"simple_cron_type\":\"day\",\"simple_cron_value\":31}",
                "cron": "0 0 0 19/31 * ? *",
                "tableId":  dataset_id["id"]
            },
            "datasetTableIncrementalConfig": {
                "id": None,
                "tableId": dataset_id["id"],
                "incrementalDelete": None,
                "incrementalAdd": ""
            }
        }
        rsp = s.post(base_url+"/dataset/task/save", data=json.dumps(data), headers=headers)
        print(rsp.text)
        print(json.dumps(data))

# 查询数据集同步任务
def dataset_task_list():
    return s.post(base_url+"/dataset/task/list", data=json.dumps({}), headers=headers)

# 将数据集同步任务信息写入csv文件供性能测试脚本使用
def write_sycn_testdata():
    datas = json.loads(dataset_task_list().text)["data"]
    # wb = Workbook()
    # ws = wb.active
    # with open("data_1.csv", "w", encoding="utf-8", newline='') as f:
    #     fieldnames = ['id', 'tableId', 'name', 'type', 'startTime', 'rate', 'cron', 'end', 'endTime',
    #                   'createTime', 'lastExecTime', 'status', 'lastExecStatus', 'extraData']
    #     writer = csv.DictWriter(f, fieldnames=fieldnames)
    #     writer.writeheader()
    #     for data in datas:
    #         if data["name"] == "rask_1":
    #             writer.writerow(data)
    #
    # with open("data_10.csv", "w", encoding="utf-8", newline='') as f:
    #     fieldnames = ['id', 'tableId', 'name', 'type', 'startTime', 'rate', 'cron', 'end', 'endTime',
    #                   'createTime', 'lastExecTime', 'status', 'lastExecStatus', 'extraData']
    #     writer = csv.DictWriter(f, fieldnames=fieldnames)
    #     writer.writeheader()
    #     for data in datas:
    #         if data["name"] == "rask_10":
    #             writer.writerow(data)
    #
    # with open("data_100.csv", "w", encoding="utf-8", newline='') as f:
    #     fieldnames = ['id', 'tableId', 'name', 'type', 'startTime', 'rate', 'cron', 'end', 'endTime',
    #                   'createTime', 'lastExecTime', 'status', 'lastExecStatus', 'extraData']
    #     writer = csv.DictWriter(f, fieldnames=fieldnames)
    #     writer.writeheader()
    #     for data in datas:
    #         if data["name"] == "rask_100":
    #             writer.writerow(data)
    #
    # with open("data_1000.csv", "w", encoding="utf-8", newline='') as f:
    #     fieldnames = ['id', 'tableId', 'name', 'type', 'startTime', 'rate', 'cron', 'end', 'endTime',
    #                   'createTime', 'lastExecTime', 'status', 'lastExecStatus', 'extraData']
    #     writer = csv.DictWriter(f, fieldnames=fieldnames)
    #     writer.writeheader()
    #     for data in datas:
    #         if data["name"] == "rask_1000":
    #             writer.writerow(data)

    with open("data_5000.csv", "w", encoding="utf-8", newline='') as f:
        fieldnames = ['id', 'tableId', 'name', 'type', 'startTime', 'rate', 'cron', 'end', 'endTime',
                      'createTime', 'lastExecTime', 'status', 'lastExecStatus', 'extraData']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for data in datas:
            if data["name"] == "rask_5000":
                writer.writerow(data)

def view_query():
    return s.post(base_url+"/chart/view/list",data=json.dumps({"tableId":"2651d2d5-30bb-4bbf-8e77-b5576b94c2eb",}), headers=headers)

def create_report_rask():
    with open("panels_id.csv", "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            data = {"emailContent":"",
                    "request":{"taskName":"1920*1080_10W",
                               "title":"1920*1080_10W",
                               "rateType":2,
                               "panelId":line.strip(),
                               "rateVal":"2022-01-14 20:00:00",
                               "taskType":"emailTaskHandler",
                               "recipients":"sgb87@163.com",
                               "pixel":"1920 * 1080",
                               "startTime":1644678113000}}
            s.post(base_url+"/plugin/task/save", data=json.dumps(data), headers=headers)
            print(json.dumps(data))

def delete_report_rask():
    rsp = s.post(base_url+"/plugin/task/queryTasks/1/100", data=json.dumps({}),headers=headers)
    print(rsp.text)
    tasks = json.loads(rsp.text)["data"]["listObject"]
    for task in tasks:
        s.post(base_url+"/plugin/task/delete/"+str(task["taskId"]), data=json.dumps({}), headers=headers)
def query_panel():
    return s.post(base_url+"/panel/group/tree", data=json.dumps({}), headers=headers)
def delete_panels(group_name):
    datas = json.loads(query_panel().text)["data"]
    for _ in datas:
        if _["name"] == group_name:
            for panel in _["children"]:
                s.post(base_url+"/panel/group/deleteCircle/"+panel["id"], data=json.dumps({}), headers=headers)
if __name__ == "__main__":
    login()
    # print(dataset_group()[6]["name"])
    # creat_dataset()
    # print(dataset_group())
    # create_dataset_rask()
    # write_sycn_testdata()
    # print(json.loads(view_query().text))
    # with open("/Users/ussop/test.json", "w", encoding="utf-8") as f:
    #     f.write(view_query().text)
    # rsp = view_query()
    # for i in json.loads(rsp.text)["data"]:
    #     s.post(base_url+"/chart/view/delete/"+i["id"], headers=headers)
    create_report_rask()
    # delete_report_rask()
    # delete_panels("1000W")

