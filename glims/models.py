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
@receiver(pre_save)
def save_job(sender,instance,*args,**kwargs):
    js = JSONSerializer()
    if hasattr(instance,'args'):
        instance._args = js.dumps(instance.args)
    if hasattr(instance,'config'):
        instance._config = js.dumps(instance.config)
@receiver(post_init)
def init_job(sender, **kwargs):
    js = JSONSerializer()
    job = kwargs['instance']
    if job._args is not None:
        job.args = js.loads(job._args)
    if job._config is not None:
        job.config = js.loads(job._config)

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

class DRMAAJob(Job):
    class Meta:
        proxy = True
    def run(self,**kwargs):
        pass

            
            
