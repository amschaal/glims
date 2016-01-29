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


class HstoreOrderFilter(filters.OrderingFilter):
    """
    Filter that only allows users to see their own objects.
    """
    def __init__(self,hstore_field='data'):
        #@todo: For some reason I'm not able to call this????
        self.hstore_field = hstore_field
    def get_valid_fields(self, queryset, view):
        valid_fields = super(HstoreOrderFilter, self).get_valid_fields(queryset,view)
        for field in view.request.query_params.get('ordering','').split(','):
            trimmed = field.lstrip('-')
            if trimmed.startswith("%s__"%self.hstore_field):
                valid_fields.append((trimmed,trimmed))
        return valid_fields
    def get_ordering(self, request, queryset, view):
#         print 'Valid fields'
#         print self.get_valid_fields(queryset, view)
        """
        Ordering is set by a comma delimited ?ordering=... query parameter.

        The `ordering` query parameter can be overridden by setting
        the `ordering_param` value on the OrderingFilter or by
        specifying an `ORDERING_PARAM` value in the API settings.
        """
        ordering_strings = []
        params = request.query_params.get(self.ordering_param)
        if params:
            fields = [param.strip() for param in params.split(',')]
            ordering_strings = self.remove_invalid_fields(queryset, fields, view)
#         if not ordering_strings:
#             ordering_strings = []

        # No ordering was included, or all the ordering fields were invalid
        table = queryset.model._meta.db_table
#         ordering_fields = request.query_params.get('ordering','').split(',')
        print 'ORDERING STRINGS'
        print ordering_strings
        ordering = []
        for field in ordering_strings:
            trimmed = field.lstrip('-')
#             print 'FIELD!!'
#             print field
            if trimmed.startswith("%s__"%self.hstore_field):
                parts = trimmed.split('__')
#                 print 'ORDERING....'
#                 print parts
                if field.startswith('-'):
                    ordering += [RawSQL('"%s"."%s"'%(table,self.hstore_field)+"->%s",(parts[1],)).desc()]
                else:
                    ordering += [RawSQL('"%s"."%s"'%(table,self.hstore_field)+"->%s",(parts[1],)).asc()]
            else:
                ordering.append(field)
        print 'ORDERING'
        print ordering
        if len(ordering) != 0:
            return ordering

        # No ordering was included, or all the ordering fields were invalid
        return self.get_default_ordering(view)
#     def filter_queryset(self, request, queryset, view):
#         ordering_fields = request.query_params.get('ordering','').split(',')
#         args = ()
#         for field in ordering_fields:
#             trimmed = field.lstrip('-')
#             if trimmed.startswith("%s__"%self.hstore_field):
#                 parts = trimmed.split('__')
#                 print 'ORDERING....'
#                 print parts
#                 if field.startswith('-'):
#                     args += (RawSQL(self.hstore_field+"->%s",(parts[1],)).desc(),)
#                 else:
#                     args += (RawSQL(self.hstore_field+"->%s",(parts[1],)).asc(),)
#         print args
#         if len(args)==0:
#             return queryset
#         return queryset.order_by(*args)
