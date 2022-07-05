import requests
import re
host = 'http://democenter.fit2cloud.com:40999/'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'max-age=0',
    'Cookie': 'KEYCLOAK_LOCALE=zh-CN; JSESSIONID=node013edu737o89kp1ei8jdtmnpns429.node0; FIT2CLOUD_SESSION_ID=node0ikz8fs4z4vid13wo8218n9w1a133.node0; csrftoken=vfN9EaQEfOZflmpJpbSwPDj6g6VeT6Ik1NSa9Ws4qqJgVIf8yL3HwjnZtZPjeltI; sessionid=ia5pzfreau4t73osrwe25xdzrsvwg8if',
    'Host': 'democenter.fit2cloud.com:40999',
    'Proxy-Connection': "keep-alive",
    'Referer': "'http://democenter.fit2cloud.com:40999/core/auth/logout/?next=/dashboard",
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36 Edg/94.0.992.31'
}

s = requests.Session()

r = s.get(host + 'core/auth/login/',headers=headers)
print(r.status_code)
# print(r.text)
reg = r'<input type="hidden" name="csrfmiddlewaretoken" value="(.*?)">'
pattern = re.compile(reg)

csrfmiddlewaretoken = pattern.findall(r.text)
print(csrfmiddlewaretoken)
datas = {
            'csrfmiddlewaretoken':csrfmiddlewaretoken,
            'username':'admin',
            'password':r'KwDoAasTJ5CjorPWEvWIPzFxAB0HoQ5FTIxFOw0VvTLFXVRLfaxvCgbdPl9kMy/hAeI4o3jAED1VasaQ2DGfg9STEDDn03AdhI1v5IAmhL/sCzEkyH38NIlyIRODKA3Q04qBkiHKLp1ezjsPodVwI8b3aNwmZ4tlWXTWrdAudzw='
}

r = s.post(host +'core/auth/login/', headers=headers, data=datas)
print(r.status_code)
print(r.cookies.values())
r = s.get(host + 'api/v1/xpack/license/detail')
print(r.status_code)