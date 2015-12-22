from rest_framework import viewsets
from bioinformatics.serializers import BioinfoProjectSerializer
from bioinformatics.models import BioinfoProject



class BioinfoProjectViewSet(viewsets.ModelViewSet):
    serializer_class = BioinfoProjectSerializer
#     permission_classes = [CustomPermission]
    model = BioinfoProject
    filter_fields = {'project':['exact','icontains'], 'description':['exact','icontains']}
    search_fields = ('name', 'description')
    queryset = BioinfoProject.objects.all()
#     def get_queryset(self):
#         return get_all_user_objects(self.request.user, ['view'], Project)
