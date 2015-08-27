from django_compute.callbacks import BaseCallback

class DataOutputtedCallback(BaseCallback):
    id = 'data_outputted_callback'
    @staticmethod
    def run(job, data, **kwargs):
#         BaseCallback.run(self, **kwargs)
        print "DATA DIRECTORY!!!"
        print job.data['directory']
        
JOB_CALLBACKS = {
    DataOutputtedCallback.id: DataOutputtedCallback
}
