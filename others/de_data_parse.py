import requests
import json
import csv
base_url = "http://zdscxx.moa.gov.cn:8080"
# 重点农产品期货价格
path_1 = '/nyb/getFrequencyData'
data = {
    "page":1,
    'rows':100000,
    'type':"日度数据",
    "subTyep":"重点农产品期货价格",
    "time":'["2018-02-15","2022-02-15"]'
}
params = "page=1&rows=1000000&type=%E6%9C%88%E5%BA%A6%E6%95%B0%E6%8D%AE&subType=%E5%86%9C%E4%BA%A7%E5%93%81%E6%89%B9%E5%8F%91%E4%BB%B7%E6%A0%BC&time=%5B%222018-02%22%2C%222022-02%22%5D&product="


# headers
headers = {
    "Accept":"application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding":"gzip, deflate",
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.76",
    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie":"JSESSIONID=7920C7F21C694B70803F3A33FB69AC48; yfx_c_g_u_id_10002896=_ck22021414374210693207316835045; yfx_f_l_v_t_10002896=f_t_1644820662063__r_t_1644820662063__v_t_1644820662063__r_c_0"
}
rsp = requests.post(base_url+path_1, headers=headers,params=params)
datas = json.loads(rsp.text)
prices = datas["result"]["pageInfo"]["table"]
# print(type(prices))
# print(prices[0].values())
with open("农产品批发价格-月度数据.csv", "w", encoding="utf-8", newline='') as f:
    fieldnames = list(prices[0].keys())
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for price in prices:
        # content = price.values()
        # print(content)
        writer.writerow(price)