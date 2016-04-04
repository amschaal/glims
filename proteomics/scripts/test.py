#!/usr/bin/env python

#--------------------------------------
# SGE directives
#$ -S /usr/bin/python
#$ -t 1-3
#--------------------------------------

import os, urllib2, json, time
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

print os.environ.keys()
print 'TASK ID: %s' % os.environ['SGE_TASK_ID']
time.sleep(120)
if os.environ['SGE_TASK_ID'] != '':
    job_id = "%s.%s" % (os.environ['JOB_ID'],os.environ['SGE_TASK_ID'])
else:
    job_id = os.environ['JOB_ID']
LIMSJob.update(job_id,LIMSJob.RUNNING,data={'stage':1}) 
print "Hi python!"
LIMSJob.update(job_id,LIMSJob.RUNNING,data={'stage':2}) 
print "Bye world!"
LIMSJob.update(job_id,LIMSJob.DONE,data={'stage':3})

