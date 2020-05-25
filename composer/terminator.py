import yaml
import json
import requests
import datetime as dt

'''
parapide: 172.16.98.xx
paravance: 172.16.96.xx
petitprince: 172.16.177.xx
uvb: 172.16.132.xx
econome: 172.16.192.xx

'''

base_url = "http://localhost:5000"

def delete_jobs(url):
    delete = requests.delete(url + "/jobs")
    print(delete.status_code)


n1=dt.datetime.now()
delete_jobs(base_url)
n2=dt.datetime.now()
print(n2-n1)