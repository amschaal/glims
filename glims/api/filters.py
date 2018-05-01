from rest_framework import filters
from django.db.models.query_utils import Q
import operator
from glims.models import Project
from glims.views import project


class FollowingProjectFilter(filters.BaseFilterBackend):
    """
    Filter projects so that user only sees projects that they are managing, participating in, or subscribed to
    """
    def filter_queryset(self, request, queryset, view):
        following = view.request.query_params.get('following',None)
        if not following:
            return queryset
        project_ids = [int(id) for id in Project.objects.filter(participants__id=request.user.id).values_list('id',flat=True)]
        clauses = [Q(manager=request.user)]#,Q(participants__id=request.user.id)
#         try:
        from notifications.models import UserSubscription
        from django.contrib.contenttypes.models import ContentType
        ct = ContentType.objects.get_for_model(Project)
        project_ids += [int(id) for id in UserSubscription.objects.filter(user=request.user,content_type=ct,subscribed=True).values_list('object_id',flat=True)]
        clauses.append(Q(id__in=project_ids)) 
#         except Exception, e:
#             pass
        query = reduce(operator.or_,clauses)
        queryset =  queryset.filter(query)
        return queryset

class ParticipantFilter(filters.BaseFilterBackend):
    """
    Filter participants by first or last names, including also manager.
    """
    def filter_queryset(self, request, queryset, view):
        participant = view.request.query_params.get('participant',None)
        if not participant:
            return queryset
        project_ids = [int(id) for id in Project.objects.filter(Q(participants__first_name__icontains=participant)|Q(participants__last_name__icontains=participant)|Q(manager__last_name__icontains=participant)|Q(manager__first_name__icontains=participant)).values_list('id',flat=True)]
        queryset =  queryset.filter(id__in=project_ids)
        return queryset

class ProjectStatusFilter(filters.BaseFilterBackend):
    """
    filter by status name or 'none' to see null status
    """
    def filter_queryset(self, request, queryset, view):
        status = view.request.query_params.get('status',None)
        if not status:
            return queryset
        if status.upper() in ['NONE','BLANK','EMPTY','NULL']:
            return queryset.filter(status__isnull=True)
        else:
            return queryset.filter(status__name__icontains=status)

class MultiFilter(filters.BaseFilterBackend):
    """
    Set multi_filters property like:
    multi_filters = ['id__in']
    
    You can then use a querystring like:
    ?id__in=1&id__in=2&id__in=3
    """
    def filter_queryset(self, request, queryset, view):
        multi_filters = getattr(view, 'multi_filters',[])
        filters = {}
        for mf in multi_filters:
            val = view.request.query_params.getlist(mf,None)
            if val:
                filters[mf]=val
        if len(filters):
            queryset = queryset.filter(**filters)
        return queryset