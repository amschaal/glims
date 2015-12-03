class BaseStorageEngine:
    def __init__(self,cloudstore):
        self.cloudstore = cloudstore
#     def run(self):
#         if self.run.im_func == BaseJobEngine.run.im_func:
#             raise NotImplementedError('Run method not implemented for this job engine.')
#         self.job.status = Job.STATUS_STARTED
#         self.job.save()
#     def terminate(self):
#         if self.terminate.im_func == BaseJobEngine.terminate.im_func:
#             raise NotImplementedError('Terminate method not implemented for this job engine.')
#         self.job.status = Job.STATUS_TERMINATED
#         self.job.save()

# class StoreEngineFactory:
#     @staticmethod
#     def create(job):
#         if job.template.engine == JobTemplate.ENGINE_LOCAL:
#             from django_compute.engines.local import LocalJobEngine
#             return LocalJobEngine(job)
#         raise JobTypeException