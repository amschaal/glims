from django_compute.callbacks import BaseCallback

class TandemCallback(BaseCallback):
    id = 'tandem_callback'
    @staticmethod
    def run(job, data, **kwargs):
#         BaseCallback.run(self, **kwargs)
        print "DATA DIRECTORY!!!"
        print job.data
        print job.output_directory
        
JOB_CALLBACKS = {
    TandemCallback.id: TandemCallback
}
