from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONPRenderer, JSONRenderer
from glims.job import JobFactory
# from models import 
from django.core.exceptions import ObjectDoesNotExist
@api_view(['POST'])
# @permission_classes((ServerAuth, ))  
def update_job(request, job_id):
    status = request.DATA.get('status')
    job = JobFactory.get_job(job_id)
    job.update_status(status)
    return Response({})
