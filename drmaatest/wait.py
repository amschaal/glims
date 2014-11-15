#!/usr/bin/env python

import drmaa
import os
OPATH=":"+drmaa.JobTemplate.HOME_DIRECTORY+'/DRMAA_JOB_OUT'
def main():
    """Submit a job and wait for it to finish.
    Note, need file called sleeper.sh in home directory.
    """
    s = drmaa.Session()
    s.initialize()
    print 'Creating job template'
    jt = s.createJobTemplate()
    jt.remoteCommand = '/home/adam/sleeper.sh'#os.getcwd() + '/sleeper.sh'
    jt.args = ['42','Simon says:']
    jt.email = 'amschaal@ucdavis.edu'
    jt.joinFiles = True
#    jt.outputPath=OPATH
    
    jobid = s.runJob(jt)
    print 'Your job has been submitted with id ' + jobid

    retval = s.wait(jobid, drmaa.Session.TIMEOUT_WAIT_FOREVER)
    print 'Job: ' + str(retval.jobId) + ' finished with status ' + str(retval.hasExited)

    print 'Cleaning up'
    s.deleteJobTemplate(jt)
    s.exit()
    
if __name__=='__main__':
    main()
