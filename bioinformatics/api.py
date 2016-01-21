from rest_framework import viewsets
from bioinformatics.serializers import BioinfoProjectSerializer 
from bioinformatics.models import BioinfoProject
from rest_framework.decorators import list_route, detail_route
from django.contrib.auth.models import User
from glims.serializers import UserSerializer
from rest_framework.response import Response



class BioinfoProjectViewSet(viewsets.ModelViewSet):
    serializer_class = BioinfoProjectSerializer
#     permission_classes = [CustomPermission]
    model = BioinfoProject
    filter_fields = {'project':['exact','icontains'],'name':['exact','icontains'], 'description':['exact','icontains'],'project__lab__name':['exact','icontains'],'project__name':['exact','icontains'],'manager':['exact'],'project__status__id':['icontains','exact']}
    ordering_fields = ('name','project__name', 'project__lab__name','created','manager__first_name','manager__last_name','project__status')
    queryset = BioinfoProject.objects.all().select_related('project','manager')
    @list_route()
#     @detail_route(methods=['get'])
    def users(self, request, pk=None):
        users = User.objects.filter(groups__id=1)

        page = self.paginate_queryset(users)
        if page is not None:
            serializer = UserSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
#     def get_serializer_class(self):
#         if self.request.method in ['PATCH', 'POST', 'PUT']:
#             return BioinfoProjectSerializerWrite
#         else:
#             return BioinfoProjectSerializerRead
#     def get_serializer(self, *args, **kwargs):
#         serializer_class = self.get_serializer_class()
#         context = self.get_serializer_context()
#         return serializer_class(*args, request_user=self.request.user, context=context, **kwargs)
#     def get_queryset(self):
#         return get_all_user_objects(self.request.user, ['view'], Project)
