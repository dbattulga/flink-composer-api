# Flink Composer API

### Pull the repository and run docker-compose

## Usage

**2 endpoints:**

- `/jobs` GET and POST
- `/jobs/<name>` GET and DELETE 

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
    "location": "http://localhost:8081",
    "mqtt": "tcp://localhost:1883",
    "source": "T-1",
    "sink": "T-2",
    "class": "flinkpackage.FlowCheck"
  },
  {
    "jobname": "B",
    "version": 1,
    "jarid": "97888c54-1d69-44b7-8586-15ba0ae1b7b3_flinktest-1.jar",
    "jobid": "a5cf9ff2bab498f755f49c144e5044c7",
    "location": "http://localhost:8081",
    "mqtt": "tcp://localhost:1883",
    "source": "T-2",
    "sink": "T-N",
    "class": "flinkpackage.FlowCheck"
  }
]
```

### Registering a new job

**Definition**

`POST /jobs`

**Arguments**

- `"job_name":string` unique name for this job
- `"version":string` job version
- `"flink_address":string` the IP address of the Flink instance
- `"mqtt_address":string` the IP address of main MQTT broker
- `"source_topic":string` subscriber topic of the job
- `"sink_topic":string` publisher topic of the job
- `"entry_class":string` entry class of the JAR if it contains multiple
- `"jar_path":string` link to local directory of the existing JAR file

**Response**

- `201 Created` on success

```json
  {
    "jobname": "A",
    "version": 1,
    "jarid": "97888c54-1d69-44b7-8586-15ba0ae1b7b3_flinktest-1.jar",
    "jobid": "a5cf9ff2bab498f755f49c144e5044c7",
    "location": "http://localhost:8081",
    "mqtt": "tcp://localhost:1883",
    "source": "T-2",
    "sink": "T-N",
    "class": "flinkpackage.FlowCheck"
  }
```

## Lookup jobs details

`GET /jobs/<name>`

**Response**

- `404 Not Found` if the job does not exist
- `200 OK` on success

```json
  {
    "jobname": "B",
    "version": 1,
    "jarid": "97888c54-1d69-44b7-8586-15ba0ae1b7b3_flinktest-1.jar",
    "jobid": "a5cf9ff2bab498f755f49c144e5044c7",
    "location": "http://localhost:8081",
    "mqtt": "tcp://localhost:1883",
    "source": "T-2",
    "sink": "T-N",
    "class": "flinkpackage.FlowCheck"
  }
```

## Delete a job

**Definition**

`DELETE /jobs/<name>`

**Response**

- `404 Not Found` if the job does not exist
- `204 No Content` on success