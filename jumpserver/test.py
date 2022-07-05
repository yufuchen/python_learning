import datetime

X_JMS_ORG = "00000000-0000-0000-0000-000000000000"
GMT_FORM = '%a, %d %b %Y %H:%M:%S GMT'
headers = {
    'Accept': 'application/json',
    'X-JMS-ORG': X_JMS_ORG,
    'Date': None
}

headers['Date'] =datetime.datetime.utcnow().strftime(GMT_FORM)
print(headers)