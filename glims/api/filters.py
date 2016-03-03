from django.db.models.expressions import RawSQL

from rest_framework import filters

class HstoreFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
#         @todo: This could probably be more secure... (it takes any filter starting with "data__")
        print 'HSTORE FILTER'
        hstore_field = getattr(view, 'hstore_field', None)
        print hstore_field
        if not hstore_field:
            return queryset
        print hstore_field
        filters = {}
        for key,value in request.query_params.items():
            if key.startswith('%s__'%hstore_field) and value:
                filters[key]=value
        print filters
        return queryset.filter(**filters)


class HstoreOrderFilter(filters.OrderingFilter):
    """
    Filter that only allows users to see their own objects.
    """
    def get_valid_fields(self, queryset, view):
        hstore_field = getattr(view, 'hstore_field', None)
        if not hstore_field:
            return super(HstoreOrderFilter, self).get_valid_fields(queryset,view)
        valid_fields = super(HstoreOrderFilter, self).get_valid_fields(queryset,view)
        for field in view.request.query_params.get('ordering','').split(','):
            trimmed = field.lstrip('-')
            if trimmed.startswith("%s__"%hstore_field):
                valid_fields.append((trimmed,trimmed))
        return valid_fields
    def get_ordering(self, request, queryset, view):
        hstore_field = getattr(view, 'hstore_field', None)
        if not hstore_field:
            return super(HstoreOrderFilter, self).get_ordering(request,queryset,view)
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

        # No ordering was included, or all the ordering fields were invalid
        table = queryset.model._meta.db_table
        ordering = []
        for field in ordering_strings:
            trimmed = field.lstrip('-')
            if trimmed.startswith("%s__"%hstore_field):
                parts = trimmed.split('__')
                if field.startswith('-'):
                    ordering += [RawSQL('"%s"."%s"'%(table,hstore_field)+"->%s",(parts[1],)).desc()]
                else:
                    ordering += [RawSQL('"%s"."%s"'%(table,hstore_field)+"->%s",(parts[1],)).asc()]
            else:
                ordering.append(field)
        if len(ordering) != 0:
            return ordering
        # No ordering was included, or all the ordering fields were invalid
        return self.get_default_ordering(view)
