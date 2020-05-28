# Flink Composer API

### Before running, don't forget to start MQTT broker and Flink instances
`docker run -dit -p 1883:1883 -p 9001:9001 eclipse-mosquitto`

### Pull the repository and run 
`docker-compose up -d`

## Usage

**2 endpoints:**

- `/jobs` GET and POST
- `/jobs/<name>` GET and DELETE 

### Register a new job

**Definition**

`POST /jobs`

**Arguments**

- `"job_name":string` unique name for this job
- `"version":string` job version
- `"flink_address":string` the IP address of the Flink instance
- `"source_mqtt":string` the IP address of source MQTT broker
- `"sink_mqtt":string` the IP address of sink MQTT broker
- `"source_topic":string` subscriber topic of the job
- `"sink_topic":string` publisher topic of the job
- `"entry_class":string` entry class of the JAR if it contains multiple
- `"jar_path":string` link to local directory of the existing JAR file

**Example**

```json
  {
    "job_name": "A",
    "version": "1",
    "flink_address": "http://10.188.166.98:8081",
    "source_mqtt": "tcp://10.188.166.98:1883",
    "sink_mqtt": "tcp://10.188.166.98:1883",
    "source_topic": "T-1",
    "sink_topic": "T-N",
    "entry_class": "flinkpackage.FlowCheck",
    "jar_path": "/usr/src/app/jars/flinktest-1.jar"
  }
```

**Response**

- `201 Created` on success

```json
  {
    "jobname": "A",
    "version": 1,
    "jarid": "97888c54-1d69-44b7-8586-15ba0ae1b7b3_flinktest-1.jar",
    "jobid": "a5cf9ff2bab498f755f49c144e5044c7",
    "location": "http://10.188.166.98:8081",
    "source_mqtt": "tcp://10.188.166.98:1883",
    "sink_mqtt": "tcp://10.188.166.98:1883",
    "source_topic": "T-1",
    "sink_topic": "T-N",
    "class": "flinkpackage.FlowCheck"
  }
```

### List all Jobs

**Definition**

`GET /jobs`

**Response**

- `200 OK` on success

```json
[
  {
    "jobname": "A",
    "version": 1,
    "jarid": "97888c54-1d69-44b7-8586-15ba0ae1b7b3_flinktest-1.jar",
    "jobid": "a5cf9ff2bab498f755f49c144e5044c7",
    "location": "http://10.188.166.98:8081",
    "source_mqtt": "tcp://10.188.166.98:1883",
    "sink_mqtt": "tcp://10.188.166.98:1883",
    "source_topic": "T-1",
    "sink_topic": "T-N",
    "class": "flinkpackage.FlowCheck"
  },
  {
    "jobname": "B",
    "version": 2,
    "jarid": "97888c54-1d69-44b7-8586-15ba0ae1b7b3_flinktest-1.jar",
    "jobid": "a5cf9ff2bab498f755f49c144e5044c7",
    "location": "http://10.188.166.98:8081",
    "source_mqtt": "tcp://10.188.166.98:1883",
    "sink_mqtt": "tcp://10.188.166.98:1883",
    "source_topic": "T-2",
    "sink_topic": "T-N",
    "class": "flinkpackage.FlowCheck"
  }
]
```

## Lookup jobs details

`GET /jobs/<name>`

**Response**

- `404 Not Found` if the job does not exist
- `200 OK` on success

```json
  {
    "jobname": "A",
    "version": 1,
    "jarid": "97888c54-1d69-44b7-8586-15ba0ae1b7b3_flinktest-1.jar",
    "jobid": "a5cf9ff2bab498f755f49c144e5044c7",
    "location": "http://10.188.166.98:8081",
    "source_mqtt": "tcp://10.188.166.98:1883",
    "sink_mqtt": "tcp://10.188.166.98:1883",
    "source_topic": "T-1",
    "sink_topic": "T-N",
    "class": "flinkpackage.FlowCheck"
  }
```

## Delete a job

**Definition**

`DELETE /jobs/<name>`

**Response**

- `404 Not Found` if the job does not exist
- `204 No Content` on success