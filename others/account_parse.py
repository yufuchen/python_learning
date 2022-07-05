import json
with open("data.txt", 'r') as file:
    data = file.read()
# account_list = json.loads(data)
account_list = json.loads(data)["data"]["listObject"]
# print(account_list)
account_ids = []
for account in account_list:
    # vars.put("account_id"+str(count), account["id"])
    # count += 1
    account_ids.append(account["id"])
print(type(json.dumps(account_ids)))

# var.put("account_ids", json.dumps(account_ids))