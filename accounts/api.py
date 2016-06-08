from rest_framework import viewsets
# from models import 
from accounts.models import Account
from accounts.serializers import AccountSerializer

class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
#     permission_classes = [CustomPermission]
#     search_fields = ('name', 'description')
    model = Account
    filter_fields = ('project',)
    queryset = Account.objects.all()
#     def get_queryset(self):
#         return File.objects.all()
