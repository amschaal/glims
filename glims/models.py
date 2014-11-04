from django.db import models
from django.contrib.auth.models import User
from glims.settings import ADMIN_EMAIL

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
class Job(models.Model):
    type = models.CharField(max_length=50)
    name = models.CharField(max_length=100,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    status = models.CharField(max_length=50,blank=True,null=True)
    path = models.CharField(max_length=250)
    job_id = models.CharField(max_length=30,blank=True,null=True)
    _args = models.TextField(blank=True,null=True)
    _config = models.TextField(blank=True,null=True)
#     def __init__(self, job):
#         self.job = job
    def run(self,**kwargs):
        pass
    """
    update_status is called via REST API
    
    """
    def update_status(self, status, **kwargs):
        self.job.status = status
        self.job.save()
        """
        if status == 'foo':
            do bar
        elif status == 'yin':
            do yang
        """
@receiver(pre_save, sender=Job)
def save_job(sender,instance,*args,**kwargs):
    js = JSONSerializer()
    if hasattr(instance,'args'):
        instance._args = js.dumps(instance.args)
    if hasattr(instance,'config'):
        instance._config = js.dumps(instance.config)
@receiver(post_init, sender=Job)
def init_job(sender, **kwargs):
    js = JSONSerializer()
    job = kwargs['instance']
    if job._args is not None:
        job.args = js.loads(job._args)
    else:
        job.args = []
    if job._config is not None:
        job.config = js.loads(job._config)
    else:
        job.config = {}

class JobFactory:
    @staticmethod
    def create_job(cls,**kwargs):
        js = JSONSerializer()
        if kwargs.has_key('args'):
            kwargs['_args'] = js.dumps(kwargs['args'])
        kwargs['type']=cls.__name__
        return cls.objects.create(**kwargs)
    @staticmethod
    def get_job(id):
        job = Job.objects.get(id=id)
        cls = globals()[job.type]
        return cls.objects.get(id=id)

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
        #jt.joinFiles = True
        self.jt = jt
        return jt
    def run(self,cleanup=True):
        self.start_session()
        jt = self.create_template()
        if hasattr(self,'native_specification'):
            jt.nativeSpecification = self.native_specification
        self.job_id = self.session.runJob(jt)
        print "Job created: " + self.job_id
        # Disable this option if you want to use get_drmaa_status
        if cleanup:
            self.exit()
    #Buggy: Only seems to work with SGE when the session has not been exited
    def get_drmaa_status(self):
        if self.job_id:
            self.start_session()
            status = self.session.jobStatus(self.job_id)
            return DRMAAJob.DRMAA_STATE[status] 
        else:
            return "No job id yet available."
            
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
        self.native_specification = '-b n' #Submit job as script, not binary.  Makes SGE copy script over.
        
            
            
