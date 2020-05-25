import yaml
import random


num_of_jobs = 100
list_of_versions = [1, 2]
mqtt_address = 'tcp://172.16.96.52:1883'
entry_class = 'flinkpackage.FlowCheck'
jar_path = '/usr/src/app/jars/flinktest-1.jar'

with open('random_job_list.txt') as f:
    list_of_job_names = f.readlines()
list_of_job_names = [x.strip() for x in list_of_job_names]
#list_of_job_names = ['A', 'B', 'C', 'D']


with open('active_instances.txt') as f:
    list_of_instances = f.readlines()
list_of_instances = [x.strip() for x in list_of_instances]

list_of_topics = []
for number in range(num_of_jobs):
     topic = 'T-'+str(number+1)
     list_of_topics.append(topic)
list_of_topics.append('T-N')

jobs_list = []

def generate_job():
     temp = []
     for name in jobs_list:
          temp.append(name['job_name'])
     while True:
          job_name = random.choice(list_of_job_names)
          if job_name not in temp:
               break


     version = random.choice(list_of_versions)
     #version = 1
     flink_address = random.choice(list_of_instances)
     source_topic = random.choice(list_of_topics)
     sink_topic = random.choice(list_of_topics)
     job = {'job_name': job_name,
          'version': version,
          'flink_address': flink_address,
          'mqtt_address': mqtt_address,
          'source_topic': source_topic,
          'sink_topic': sink_topic,
          'entry_class': entry_class,
          'jar_path': jar_path
          }
     return job

for jobs in range(num_of_jobs):
     job = generate_job()
     jobs_list.append(job)

dict = {'jobs' :jobs_list}

with open('result.yaml', 'w') as yaml_file:
    yaml.dump(dict, yaml_file, default_flow_style=False, sort_keys=False)
