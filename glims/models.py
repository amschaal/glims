from django.db import models
from django.contrib.auth.models import User
from glims.settings import ADMIN_EMAIL
from jsonfield import JSONField
import string, random
from extensible.models import ModelType

    
class Plugin(models.Model):
    id = models.CharField(max_length=50,primary_key=True)
    app = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    description = models.TextField()
    page = models.CharField(max_length=50) #choices= Project, Sample, Experiment
    template = models.CharField(max_length=250) #template to render
    model_types = models.ManyToManyField(ModelType,null=True,blank=True, through='ModelTypePlugins',related_name='plugins')
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


