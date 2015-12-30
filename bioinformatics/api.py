from rest_framework import viewsets
from bioinformatics.serializers import BioinfoProjectSerializer
from bioinformatics.models import BioinfoProject



class BioinfoProjectViewSet(viewsets.ModelViewSet):
    serializer_class = BioinfoProjectSerializer
#     permission_classes = [CustomPermission]
    model = BioinfoProject
    filter_fields = {'project':['exact','icontains'], 'description':['exact','icontains'],'project__lab__name':['exact','icontains'],'assigned_to':['exact'],'project__status__id':['icontains','exact']}
    ordering_fields = ('project__name', 'project__lab__name','created','assigned_to__first_name','assigned_to__last_name','project__status')
    queryset = BioinfoProject.objects.all().select_related('project','assigned_to')
#     def get_queryset(self):
#         return get_all_user_objects(self.request.user, ['view'], Project)
