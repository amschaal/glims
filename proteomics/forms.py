from django.conf import settings
from django import forms
from proteomics.models import FastaFile, ParameterFile
from glims.lims import Sample

class FastaFileForm(forms.ModelForm):
    file_url = forms.URLField(required=False)
    class Meta:
        model = FastaFile
        exclude = ('uploaded_by','count','modified')
    def download_file(self):
        if not self.cleaned_data['file_url']:
            return
        import urllib2, cgi
        from django.core.files import File
        from django.core.files.temp import NamedTemporaryFile
        from urlparse import urlparse
        temp = NamedTemporaryFile(delete=True)
        file_url = self.cleaned_data.get("file_url")
        print file_url
        remote_file = urllib2.urlopen(file_url)
        temp.write(remote_file.read())
        temp.flush()
        _, params = cgi.parse_header(remote_file.headers.get('Content-Disposition', ''))
        filename = params['filename'] if params.has_key('filename') else '%s.fasta' % self.cleaned_data['name'] 
#         name = remote_file.info()['Content-Disposition']
#         name = urlparse(file_url).path.split('/')[-1]
        self.instance.file.save(filename,File(temp))
        print self.instance
        print "Saved!"
#         from django.core.files import File
#         import urllib
#         path = settings.MEDIA_ROOT
#         file_url = cleaned_data.get("file_url")
#         
#         urllib.urlretrieve ("http://www.example.com/songs/mp3.mp3", "mp3.mp3")
#         print "Downloading %s" % self.cleaned_data['file_url']
    def clean(self):
            cleaned_data=super(FastaFileForm, self).clean()
            file_url = cleaned_data.get("file_url")
            file = cleaned_data.get("file")
            if not file_url and not file:
                raise forms.ValidationError("Either a file or a file URL is required!")
            return cleaned_data
        
class TandemForm(forms.Form):
    samples = forms.ModelMultipleChoiceField(queryset=Sample.objects.all())
    parameter_file = forms.ModelChoiceField(queryset=ParameterFile.objects.all())
    fasta_file = forms.ModelChoiceField(queryset=FastaFile.objects.all())
#     threads = forms.IntegerField(min_value=1,max_value=16)
#     xtandem = forms.BooleanField(label="X!Tandem")
#     msgf = forms.BooleanField(label="MS-GF+")
#     omssa = forms.BooleanField(label="OMSSA")
#     ms_amanda = forms.BooleanField(label="MS Amanda")
#     myrimatch = forms.BooleanField(label="MyriMatch")
#     comet = forms.BooleanField(label="Comet")
#     tide = forms.BooleanField(label="Tide")

