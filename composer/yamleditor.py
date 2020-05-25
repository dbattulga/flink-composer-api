import yaml
import random


num_of_jobs = 100
list_of_versions = [1, 2]
mqtt_address = 'tcp://172.16.96.52:1883'
entry_class = 'flinkpackage.FlowCheck'
jar_path = '/usr/src/app/jars/flinktest-1.jar'

with open('active_instances.txt') as f:
    list_of_instances = f.readlines()
list_of_instances = [x.strip() for x in list_of_instances]

list_of_topics = []
for number in range(num_of_jobs):
     topic = 'T-'+str(number+1)
     list_of_topics.append(topic)
list_of_topics.append('T-N')


job_names = []
with open('result.yaml') as f:
    list_of_jobs = yaml.load(f)
userjobs = list_of_jobs['jobs']

for userjob in list_of_jobs['jobs']:
    job_names.append(userjob['job_name'])


#print(userjobs)

def edit_job(job_name):
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

temp = []
while True:
    j_name = random.choice(job_names)
    if ((not temp) or (j_name not in temp)):
        temp.append(j_name)
        for i in range(len(userjobs)):
            #print(userjobs[i])
            if (userjobs[i]['job_name'] == j_name):
                job = edit_job(j_name)
                userjobs[i] = job
    print(len(temp))
    if len(temp) == num_of_jobs:
        break

#print(userjobs)

dict = {'jobs' :userjobs}

with open('result.yaml', 'w') as yaml_file:
#with open('result-edited.yaml', 'w') as yaml_file:
    yaml.dump(dict, yaml_file, default_flow_style=False, sort_keys=False)
