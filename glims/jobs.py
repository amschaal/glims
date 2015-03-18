from django.db import models
from django.contrib.auth.models import User
from glims.settings import ADMIN_EMAIL
from jsonfield import JSONField
import string, random, os


def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class JobSubmission(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    submitter = models.ForeignKey(User)
    job_name = models.CharField(max_length=100,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    @staticmethod
    def create(id_prefix,kwargs={}):
        kwargs['id'] = "%s_%s" % (id_prefix,id_generator(size=10))
        return JobSubmission(**kwargs)
    def create_directory(self,root_directory):
        directory = os.path.join(root_directory,self.id)
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory
    class Meta:
        app_label = 'glims'
    
class Job(models.Model):
    submission = models.ForeignKey(JobSubmission,related_name="jobs",blank=True,null=True)
    type = models.CharField(max_length=50)
    name = models.CharField(max_length=100,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    status = models.CharField(max_length=50,blank=True,null=True)
    path = models.CharField(max_length=250)
    job_id = models.CharField(max_length=75,blank=True,null=True)
    args = JSONField(blank=True,null=True, default=[])
    config = JSONField(blank=True,null=True, default={})
    data = JSONField(blank=True,null=True, default={})
    created = models.DateTimeField(auto_now=True)
    class Meta:
        app_label = 'glims'
#     def __init__(self, job):
#         self.job = job
    def run(self,**kwargs):
        pass
    """
    update_status is called via REST API
    
    """
    #Hold job on job(s) identified by id or name
    def hold_on(self,job_id):
        self.config['hold']=job_id
    def update_status(self, status, **kwargs):
        self.status = status
        self.save()
        """
        if status == 'foo':
            do bar
        elif status == 'yin':
            do yang
        """



class JobFactory:
    @staticmethod
    def create_job(cls,**kwargs):
#         js = JSONSerializer()
#         if kwargs.has_key('args'):
#             kwargs['_args'] = js.dumps(kwargs['args'])
        kwargs['type']=cls.__name__
        return cls.objects.create(**kwargs)
    @staticmethod
    def create_job_array(cls,begin, end, step,**kwargs):
        template_job = JobFactory.create_job(cls,**kwargs)
        ids = template_job.run_array_job(begin,end,step)
        template_job.delete()
        jobs = []
        for id in ids:
            job = JobFactory.create_job(cls,**kwargs)
            job.job_id = id
            job.save()
            jobs.append(job)
        return jobs
    @staticmethod
    def get_job(job_id):
        job = Job.objects.get(job_id=job_id)
        print 'type'
        print job.type
        cls = globals()[job.type]
        return cls.objects.get(job_id=job_id)

# class Job(object):

class ClusterJob(Job):
    class Meta:
        proxy = True
    def run(self,**kwargs):
        pass

"""
ClusterJob will probably be extended for a more specific clustering software, ie:

class SGEJob(ClusterJob):
    def run(self,**kwargs):
        ...
"""

import drmaa

class DRMAAJob(Job):
    class Meta:
        proxy = True
    INVALID = 'invalid'
    DRMAA_STATE = {
        drmaa.JobState.UNDETERMINED: 'process status cannot be determined',
        drmaa.JobState.QUEUED_ACTIVE: 'job is queued and active',
        drmaa.JobState.SYSTEM_ON_HOLD: 'job is queued and in system hold',
        drmaa.JobState.USER_ON_HOLD: 'job is queued and in user hold',
        drmaa.JobState.USER_SYSTEM_ON_HOLD: 'job is queued and in user and system hold',
        drmaa.JobState.RUNNING: 'job is running',
        drmaa.JobState.SYSTEM_SUSPENDED: 'job is system suspended',
        drmaa.JobState.USER_SUSPENDED: 'job is user suspended',
        drmaa.JobState.DONE: 'job finished normally',
        drmaa.JobState.FAILED: 'job finished, but failed',
        INVALID:'job status is not available',
    }
    def __init__(self, *args, **kwargs):
        super(DRMAAJob, self).__init__(*args, **kwargs)
        if not self.config.has_key('native_specification'):
            self.config['native_specification'] = []
    def __del__(self):
        self.exit() 
#         super(DRMAAJob, self).__del__()
    def start_session(self,restore=True):
        if not hasattr(self,'session'):
            self.session = drmaa.Session()
            if self.config.has_key('session'):
                print "Initializing session: " + self.config['session']
                self.session.initialize(self.config['session'])
            else:
                self.session.initialize()
                self.config['session'] = self.session.contact
            print 'A session was started successfully'
        return self.session
    def exit(self):
        if hasattr(self,'session'):
            if hasattr(self,'jt'):
                self.session.deleteJobTemplate(self.jt)
            self.session.exit()
            del self.session
    def create_template(self):
        self.start_session()
        if not hasattr(self,'jt'):
            self.jt = self.session.createJobTemplate()
        self.jt.remoteCommand = self.path
        if hasattr(self,'args'):
            self.jt.args = self.args
        if self.config.has_key('job_name'):
            self.jt.jobName= self.config['job_name']
            print "Job name %s" % self.jt.jobName
        if self.config.has_key('working_directory'):
            self.jt.workingDirectory = self.config['working_directory']
        if self.config.has_key('native_specification'):
            self.jt.nativeSpecification = ' '.join(self.config['native_specification'])
        print 'Native'
        print self.jt.nativeSpecification
        #jt.joinFiles = True
        return self.jt
    def run(self,save=True,cleanup=True):
        jt = self.create_template()
        self.job_id = self.session.runJob(jt)
        self.status = self.get_status() 
        if save:
            self.save()
        print "Job created: " + self.job_id
        print self.config
#         print "Job specification: %s" % jt.nativeSpecification
        # Disable this option if you want to use get_drmaa_status
        if cleanup:
            self.exit()
    #returns array of job ids
    def run_array_job(self, begin=1, end=1, step=1, cleanup=True):
        jt = self.create_template()
#         print 'Native Spec' + jt.nativeSpecification
        job_ids = self.session.runBulkJobs(jt,begin, end, step)
        if cleanup:
            self.exit()
        return job_ids
    def get_status_message(self):
        return DRMAAJob.DRMAA_STATE[self.get_status()]
    def get_status(self):
        if self.job_id:
            try:
                self.start_session()
                status = self.session.jobStatus(self.job_id)
                return status#DRMAAJob.DRMAA_STATE[status]
            except drmaa.errors.InvalidJobException, e:
                return DRMAAJob.INVALID
        else:
            return DRMAAJob.INVALID
            
    #This is just for testing
    def wait(self):
        retval = self.session.wait(self.job_id, drmaa.Session.TIMEOUT_WAIT_FOREVER)
        self.status =  'Job: ' + str(retval.jobId) + ' finished with status ' + str(retval.hasExited)
        return self.status

class SGE(DRMAAJob):
    class Meta:
        proxy = True
    def __init__(self, *args, **kwargs):
        super(SGE, self).__init__(*args, **kwargs)
        self.config['native_specification'].append('-b n') #Submit job as script, not binary.  Makes SGE copy script over.
        
    def create_template(self):
        if self.config.has_key('hold'):
            self.config['native_specification'].append('-hold_jid %s' % self.config['hold'])
        super(SGE, self).create_template()
        return self.jt

class SLURM(DRMAAJob):
    class Meta:
        proxy = True
    def __init__(self, *args, **kwargs):
        super(SLURM, self).__init__(*args, **kwargs)
    def create_template(self):
        if self.config.has_key('hold'):
            self.config['native_specification'].append('--dependency=%s' % self.config['hold'])
        super(SLURM, self).create_template()
        return self.jt
            
#SLURM
#-d, --dependency=<dependency_list>            
