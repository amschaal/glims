from django.db import models
from django.contrib.auth.models import User
from glims.settings import ADMIN_EMAIL
from jsonfield import JSONField
import string, random

    
class Plugin(models.Model):
    id = models.CharField(max_length=50,primary_key=True)
    app = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    description = models.TextField()
    page = models.CharField(max_length=50) #choices= Project, Sample, Experiment
    template = models.CharField(max_length=250) #template to render
    def __unicode__(self):
        return "App: %s, Page: %s, Plugin: %s" % (self.app,self.page,self.name)


class EmailTemplate(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=250)
    body = models.TextField()

class Email(models.Model):
    created = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=250)
    body = models.TextField()
    def serialize(self):
        sent = self.recipients.filter(sent__isnull=False).count()
        unsent = self.recipients.filter(sent__isnull=True).count()
        return {'created':self.created,'subject':self.subject,'body':self.body,'sent':sent,'unsent':unsent}
    @classmethod
    def create_from_template(cls, template, to_addresses):
        return cls.create(template.subject, template.body, to_addresses)
#     @classmethod
#     def create_from_template_file(cls, template_file, to_addresses):
#         return cls.create(template.subject, template.body, to_addresses)
    @classmethod
    def create(cls, subject, body, to_addresses):
        email = cls(subject=subject, body=body)
        email.save()
        for address in to_addresses:
            EmailRecipient(email=email,address=address).save()
        return email
    def send(self,context={}):
        from django.core.mail import send_mail
        from datetime import datetime
        from django.template import Context, Template
        for er in self.recipients.filter(sent__isnull=True):
            try:
                try:
                    user = User.objects.get(email=er.address)
                    user_context = {'user':user}
                    user_context.update(context)
                    c = Context(user_context)
                except Exception, e:
                    c = Context(context)
                subject_template = Template(self.subject)
                body_template = Template(self.body)
                send_mail(subject_template.render(c), body_template.render(c), ADMIN_EMAIL, ['amschaal@gmail.com'], fail_silently=False)
                er.sent = datetime.now()
                er.save()
            except Exception, e:
                print e
class EmailRecipient(models.Model):
    email = models.ForeignKey(Email,related_name='recipients')
    address = models.CharField(max_length=75)
    sent = models.DateTimeField(auto_now=False, null=True, blank=True)
#     def generate_email(self):



# from django.db import models
from django.db.models.signals import post_init, pre_save
from django.dispatch import receiver
# import pickle
from django.contrib.sessions.serializers import JSONSerializer

# Because we are using proxy models, most information should be contained in this base class.  
# Additional information will need to be added to subclasses by using another table related by Foreign Key


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
#     def __init__(self, job):
#         self.job = job
    def run(self,**kwargs):
        pass
    """
    update_status is called via REST API
    
    """
    def update_status(self, status, **kwargs):
        self.status = status
        self.save()
        """
        if status == 'foo':
            do bar
        elif status == 'yin':
            do yang
        """
# class SubJob(models.Model):
#     job = models.ForeignKey(Job, related_name="subjobs")
#     job_id = models.CharField(max_length=30,blank=True,null=True)
#     status = models.CharField(max_length=50,blank=True,null=True)
#     data = JSONField(blank=True,null=True,default={})
#     """
#     update_status is called via REST API
#     
#     """
#     def update_status(self, status, **kwargs):
#         self.job.status = status
#         self.save()
# @receiver(pre_save, sender=Job)
# def save_job(sender,instance,*args,**kwargs):
#     js = JSONSerializer()
#     if hasattr(instance,'args'):
#         instance._args = js.dumps(instance.args)
#     if hasattr(instance,'config'):
#         instance._config = js.dumps(instance.config)
# @receiver(post_init, sender=Job)
# def init_job(sender, **kwargs):
#     js = JSONSerializer()
#     job = kwargs['instance']
#     if job._args is not None:
#         job.args = js.loads(job._args)
#     else:
#         job.args = []
#     if job._config is not None:
#         job.config = js.loads(job._config)
#     else:
#         job.config = {}



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
        jt = self.session.createJobTemplate()
        jt.remoteCommand = self.path
        if hasattr(self,'args'):
            jt.args = self.args
        if hasattr(self.config,'job_name'):
            jt.jobName= self.config['job_name']
        print self.config
        if self.config.has_key('native_specification'):
            print "Set Native"
            jt.nativeSpecification = self.config['native_specification']
        #jt.joinFiles = True
        self.jt = jt
        return jt
    def run(self,cleanup=True):
        self.start_session()
        jt = self.create_template()
        self.job_id = self.session.runJob(jt)
        self.status = self.get_status() 
#         self.save()
        print "Job created: " + self.job_id
        # Disable this option if you want to use get_drmaa_status
        if cleanup:
            self.exit()
    #returns array of job ids
    def run_array_job(self, begin=1, end=1, step=1, cleanup=True):
        self.start_session()
        jt = self.create_template()
        print 'Native Spec' + jt.nativeSpecification
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
#         if self.config.has_key('native_specification'):
#             self.config['native_specification'] += ' -b n'
#         else:
        self.config['native_specification'] = '-b n' #Submit job as script, not binary.  Makes SGE copy script over.
            
#SLURM
#-d, --dependency=<dependency_list>            
