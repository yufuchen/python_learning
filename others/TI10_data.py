import json
from openpyxl import Workbook
with open('/Users/ussop/Desktop/编辑2.json', 'r') as file:
    # data = file.read()
    data_parse = json.load(file)

wb = Workbook()
ws = wb.active
# theads = list(data_parse['data']['listObject'][0].keys())
heros = data_parse['data']['listObject']
# ws.append(theads)
for hero in heros:
    hero_datas = list(hero.values())
    ws.append(hero_datas)
wb.save('hong.xlsx')

# print(type(data_parse))
# print(len(data_parse['data']['list']))