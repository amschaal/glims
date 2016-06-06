from rest_framework import filters
from django.db.models.query_utils import Q
import operator

"""
class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer = PersonSerializer
    filter_backends = (MultiFieldFilter,)
    multi_field_filters = {'person':['first_name__icontains','last_name__icontains','email__icontains']}
"""

class MultiFieldFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filters = getattr(view, 'multi_field_filters', {})
        for param, filters in filters.iteritems():
            value = view.request.query_params.get(param,None)
            if value:
                q_objects = [Q(**dict([(filter,value)])) for filter in filters]
                queryset = queryset.filter(reduce(operator.or_, q_objects))
        return queryset
