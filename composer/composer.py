import yaml
import json
import requests
import datetime as dt

base_url = "http://localhost:5000"

'''
parapide: 172.16.98.xx
paravance: 172.16.96.xx
petitprince: 172.16.177.xx
uvb: 172.16.132.xx
econome: 172.16.192.xx

'''


def get_jobs(url):
    check = requests.get(url + "/jobs")
    sysjobs = []
    if (check.ok):
        response = json.loads(check.content)
        if len(response['data']) != 0:
            for jobs in response['data']:
                sysjobs.append(jobs['jobname'])
    return sysjobs



def run_conf():
    with open('userconf.yaml') as f:
    #with open('result.yaml') as f:
        userconf = yaml.load(f)
    sysjobs = get_jobs(base_url)

    userjobs = []
    for userjob in userconf['jobs']:
        userjobs.append(userjob['job_name'])
        print("post: "+userjob['job_name'])
        body = {'job_name': userjob['job_name'],
                  'version': userjob['version'],
                  'flink_address': userjob['flink_address'],
                  'mqtt_address': userjob['mqtt_address'],
                  'source_topic': userjob['source_topic'],
                  'sink_topic': userjob['sink_topic'],
                  'entry_class': userjob['entry_class'],
                  'jar_path': userjob['jar_path']
                  }
        start = requests.post(base_url + "/jobs", json=body)
        print(start.status_code)

    for sysjob in sysjobs:
        if sysjob not in userjobs:
            print("delete: "+sysjob)
            delete = requests.delete(base_url + "/jobs/" + sysjob)
            print(delete.status_code)


n1=dt.datetime.now()
run_conf()
n2=dt.datetime.now()
print(n2-n1)