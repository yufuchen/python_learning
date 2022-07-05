import json
import csv

with open("test_rask.json", "r", encoding="utf-8") as f:
    rsp = json.loads(f.read())

for group in rsp["data"]:
    if group["name"] == "10W":
        panels = group["children"]
with open("panels_id.csv", "w", encoding="utf-8", newline='\n') as f:
    # writer = csv.writer(f)
    for panel in panels:
        # writer.writerow(panel["id"])
        f.write(panel["id"])
        f.write("\r\n")

# print(data["data"][1])