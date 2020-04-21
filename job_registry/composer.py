import yaml
import json
import restfunctions


def run_conf():
    with open('conf.yaml') as f:
        userconf = yaml.load(f)
    with open('internalconf.json', 'r+') as f: #r+ for both read and write
        internalconf = json.load(f)

    # Init Jobs
    if len(internalconf) == 0:
        print('Init')
        for userjob in userconf['jobs']:
            add_job(userjob, internalconf)
    # Modify Running Jobs
    else:
        print('Update')
        userjobs = []
        internaljobs = []
        for userjob in userconf['jobs']:
            userjobs.append(userjob['job_name'])
        for internaljob in internalconf.items():
            internaljobs.append(internaljob[0])

        statelist = {}
        for b in range(len(internaljobs)):
            for a in range(len(userjobs)):
                if userjobs[a] == internaljobs[b]:
                    statelist[userjobs[a]] = 'edit'
                    break
                if a == len(userjobs) - 1:
                    statelist[internaljobs[b]] = 'delete'
        for c in userjobs:
            if c not in statelist:
                statelist[c] = 'add'
        print(statelist)

        for job in statelist:
            if (statelist[job] == 'add'):
                for userjob in userconf['jobs']:
                    if job == userjob['job_name']:
                        add_job(userjob, internalconf)
                        print(job+' started')

            if (statelist[job] == 'edit'):
                for internaljob in list(internalconf.items()):
                    for userjob in userconf['jobs']:
                        if job == internaljob[0] and job == userjob['job_name']:
                            edit_job(userjob, internaljob, internalconf)

            if (statelist[job] == 'delete'):
                for internaljob in list(internalconf.items()):
                    if job == internaljob[0]:
                        delete_job(job, internalconf)
                        print(job + ' deleted')

    with open('internalconf.json', 'w') as f:
        json.dump(internalconf, f)


def add_job(userjob, internalconf):
    jarid = restfunctions.upload_jar(userjob['flink_address'], userjob['jar_path'])
    jobid = restfunctions.start_jar(userjob['flink_address'], jarid, userjob['entry_class'], userjob['mqtt_address'],
                                    userjob['source_topic'], userjob['sink_topic'], userjob['job_name'])
    #print(jobid)
    temp = userjob['job_name']
    values = {'jobname': userjob['job_name'],
            'version': userjob['version'],
            'jarid': jarid,
            'jobid': jobid,
            'location': userjob['flink_address'],
            'mqtt': userjob['mqtt_address'],
            'source': userjob['source_topic'],
            'sink': userjob['sink_topic'],
            'class': userjob['entry_class']
            }
    internalconf[temp] = values


def edit_job(userjob, job, internalconf):
    if userjob['flink_address'] == job[1]['location']:
        print(job[0]+' not migrating')
        job_status = restfunctions.check_job_state(userjob['flink_address'], job[1]['jobid'])
        if job_status == 'RUNNING':
            if job[1]['version'] == userjob['version']:
                # if version is different, something's changed inside java code
                if (job[1]['mqtt'] != userjob['mqtt_address'] or
                    job[1]['source'] != userjob['source_topic'] or
                    job[1]['sink'] != userjob['sink_topic'] or
                    job[1]['class'] != userjob['entry_class']):
                    print('start ' + job[0] + ' from old jar with new parameters')
                    restfunctions.stop_job(job[1]['location'], job[1]['jobid'])

                    job[1]['jobid'] = restfunctions.start_jar(job[1]['location'],
                                                    job[1]['jarid'],
                                                    userjob['entry_class'],
                                                    userjob['mqtt_address'],
                                                    userjob['source_topic'],
                                                    userjob['sink_topic'],
                                                    userjob['job_name'])
                    job[1]['mqtt'] = userjob['mqtt_address']
                    job[1]['source'] = userjob['source_topic']
                    job[1]['sink'] = userjob['sink_topic']
                    job[1]['class'] = userjob['entry_class']
                else:
                    print('nothing is changed for ' + job[0])
            else:
                print('start ' + job[0] + ' from new jar')
                delete_job(job[0], internalconf)
                add_job(userjob, internalconf)
                print('started ' + job[0] + ' from new jar')
        else:
            print(job[0] +' is not ready, check flink instances and configs')
    else:
        print(job[0]+' is migrating')
        delete_job(job[0], internalconf)
        add_job(userjob, internalconf)
        print(job[0]+' is migrated')


def delete_job(jobname, internalconf):
    restfunctions.delete_jar(internalconf[jobname]['location'], internalconf[jobname]['jarid'])
    restfunctions.stop_job(internalconf[jobname]['location'], internalconf[jobname]['jobid'])
    del internalconf[jobname]



run_conf()

