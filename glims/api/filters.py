from rest_framework import filters
from django.db.models.query_utils import Q

class FollowingProjectFilter(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        following = view.request.query_params.get('following',None)
        if not following:
            return queryset
        query = Q(manager=request.user)|Q(participants__id=request.user.id)
        return queryset.filter(query)