#!/usr/bin/env python

#--------------------------------------
# SGE directives
#$ -S /usr/bin/python
#--------------------------------------

import os, urllib2, json, time, pickle
UPDATE_URL = "http://bowie.genomecenter.ucdavis.edu:8000/api/job/%s/update/"

class LIMSJob(object):
    UNDETERMINED = 'undetermined'
    QUEUED_ACTIVE = 'queued_active'
    SYSTEM_ON_HOLD = 'system_on_hold'
    USER_ON_HOLD = 'user_on_hold'
    USER_SYSTEM_ON_HOLD = 'user_system_on_hold'
    RUNNING = 'running'
    SYSTEM_SUSPENDED = 'system_suspended'
    USER_SUSPENDED = 'user_suspended'
    USER_SYSTEM_SUSPENDED = 'user_system_suspended'
    DONE = 'done'
    FAILED = 'failed'
    @staticmethod
    def update(job_id,status,data={}):
        params={'status':status,'data':data}
        data = json.dumps(params)
        req = urllib2.Request(UPDATE_URL%job_id,data,{'Content-Type':'application/json'})
        try:
            print urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            print e

with open('settings.txt','rb') as handle:
    SETTINGS = pickle.loads(handle.read())

job_id = os.environ['JOB_ID']


LIMSJob.update(job_id,LIMSJob.RUNNING,data={'starting_scaffold':time.time()}) 
print "SCAFFOLD"
print  SETTINGS
time.sleep(60)
LIMSJob.update(job_id,LIMSJob.DONE,data={'finished_scaffold':time.time()})

