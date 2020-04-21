import json
import requests
import os


#if successful: returns jarid, else returns "failed"
def upload_jar(base_url, jarpath):
    files = {"jarfile": ( os.path.basename(jarpath), open(jarpath, "rb"), "application/x-java-archive")}
    upload = requests.post(base_url + "/jars/upload", files=files)
    if (upload.ok):
        response = json.loads(upload.content)
        if "filename" in response:
            #print(response["filename"])
            return get_upload_id(response["filename"])
    else:
        upload.raise_for_status()
        return upload.status_code


# starts job with parameters, successful: returns jobid else "failed"
def start_jar(base_url, jarid, entryclass, mqttaddr, sourcetopic, sinktopic, jobname):
    programArgs = "--jobname "+jobname+" --mqttaddr "+mqttaddr+" --sourcetopic "+sourcetopic+" --sinktopic "+sinktopic
    #allowNonRestoredState = False
    #savepointPath = ""
    propertiess = {
        "entryClass": entryclass,
        "programArgs": programArgs
        #"savepointPath": "file:///Users/davaa/flinktest/statebackend/savepoint-7b0f64-5b4d30e60d67"
        #"savepointPath": "file%3A%2F%2F%2FUsers%2Fdavaa%2Fflinktest%2Fstatebackend"
    }
    start = requests.post(base_url + "/jars/"+jarid+"/run", json=propertiess)

    if (start.ok):
        response = json.loads(start.content)
        if "jobid" in response:
            #print(response["jobid"])
            return response["jobid"]
    else:
        start.raise_for_status()
        return start.status_code

#####################################################################################################################

def stop_job_sp(base_url, jobid, sp_path):
    propertiess = {
        "targetDirectory": "file:///Users/davaa/flinktest/statebackend",
        #"targetDirectory": "file%3A%2F%2F%2FUsers%2Fdavaa%2Fflinktest%2Fstatebackend",
        "drain": False
    }
    stop = requests.post(base_url + "/jobs/" + jobid + "/stop", json=propertiess)
    if (stop.ok):
        response = json.loads(stop.content)
        if "jobid" in response:
            print(response["jobid"])
    else:
        stop.raise_for_status()


def cancel_job_sp(base_url, jobid, sp_path):
    propertiess = {
        "target-directory": "file:///Users/davaa/flinktest/statebackend",
        #"targetDirectory": "file%3A%2F%2F%2FUsers%2Fdavaa%2Fflinktest%2Fstatebackend",
        "cancel-job": True
    }
    cancel = requests.post(base_url + "/jobs/" + jobid + "/savepoints", json=propertiess)
    if (cancel.ok):
        response = json.loads(cancel.content)
        print(response)
        #if "jobid" in response:
        #    print(response["jobid"])
    else:
        cancel.raise_for_status()


def delete_sp(base_url, sp_path):
    propertiess = {
        "savepoint-path": "file:///Users/davaa/flinktest/statebackend"
    }
    delete = requests.post(base_url + "/savepoint-disposal", json=propertiess)
    if (delete.ok):
        response = json.loads(delete.content)
        print(response)
    else:
        delete.raise_for_status()

#####################################################################################################################

def find_all(a_str, sub):
    start = 1
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches

def get_upload_id(str):
    lst = list(find_all(str, '/'))
    return (str[lst[-1]+1:])


#if exists return true, else false
def check_jar_exists(base_url, jarid):
    check = requests.get(base_url + "/jars")
    if (check.ok):
        response = json.loads(check.content)
        if "files" in response:
            #print(response["files"])
            for jar in response["files"]:
                if jar["id"] == jarid:
                    return True
                #print(jar["id"])
            return False
    else:
        check.raise_for_status()
        return check.status_code


def delete_jar(base_url, jarid):
    delete = requests.delete(base_url + "/jars/" +jarid)
    if (delete.ok):
        response = json.loads(delete.content)
        #print(response)
    else:
        delete.raise_for_status()
    return delete.status_code


#returns REST call job status as RUNNING/FAILED/CANCELED or NONEXIST, else "status code"
def check_job_state(base_url, jobid):
    check = requests.get(base_url + "/jobs")
    if (check.ok):
        response = json.loads(check.content)
        if "jobs" in response:
            #print(response["jobs"])
            for job in response["jobs"]:
                #print(job["id"] + " is: " + job["status"])
                if job["id"] == jobid:
                    return job["status"]
    else:
        check.raise_for_status()
        return check.status_code

def check_job_status(base_url, jobid):
    check = requests.get(base_url + "/jobs/" + jobid)
    if (check.ok):
        response = json.loads(check.content)
        print(response)
    else:
        check.raise_for_status()
    return check.status_code

def stop_job(base_url, jobid):
    stop = requests.patch(base_url + "/jobs/" + jobid)
    if (stop.ok):
        response = json.loads(stop.content)
        print(response)
    else:
        stop.raise_for_status()
    return stop.status_code
