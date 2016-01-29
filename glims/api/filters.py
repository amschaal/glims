from django.db.models.expressions import RawSQL

from rest_framework import filters

class HstoreFilter(filters.BaseFilterBackend):
    def __init__(self,hstore_field='data'):
        #@todo: For some reason I'm not able to call this????
        self.hstore_field = hstore_field
    def filter_queryset(self, request, queryset, view):
#         @todo: This could probably be more secure... (it takes any filter starting with "data__")
#        THIS SHOULD BE A FILTER
        filters = {}
        for key,value in request.query_params.items():
            if key.startswith('%s__'%self.hstore_field) and value:
                filters[key]=value
        print 'FILTERS!!!!'
        print filters
        return queryset.filter(**filters)

class HstoreOrderFilter(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def __init__(self,hstore_field='data'):
        #@todo: For some reason I'm not able to call this????
        self.hstore_field = hstore_field
    def filter_queryset(self, request, queryset, view):
        ordering_fields = request.query_params.get('ordering','').split(',')
        args = ()
        for field in ordering_fields:
            trimmed = field.lstrip('-')
            if trimmed.startswith("%s__"%self.hstore_field):
                parts = trimmed.split('__')
                print 'ORDERING....'
                print parts
                if field.startswith('-'):
                    args += (RawSQL(self.hstore_field+"->%s",(parts[1],)).desc(),)
                else:
                    args += (RawSQL(self.hstore_field+"->%s",(parts[1],)).asc(),)
        print args
        if len(args)==0:
            return queryset
        return queryset.order_by(*args)
