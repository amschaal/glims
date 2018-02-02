from rest_framework import filters
from django.db.models.query_utils import Q
import operator
from glims.models import Project


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
