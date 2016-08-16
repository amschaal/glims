from rest_framework import filters
from django.db.models.query_utils import Q
import operator



# class UserSubscription(models.Model):
#     user = models.ForeignKey(User,related_name='user_subscriptions')
#     content_type = models.ForeignKey(ContentType)
#     object_id = models.CharField(max_length=30) #Can be coerced into integer key if necessary
#     content_object = GenericForeignKey('content_type', 'object_id')
#     subscribed = models.BooleanField(default=True)
#     email = models.BooleanField(default=True)
#     class Meta:
#         unique_together = (("user", "content_type", "object_id"),)

class FollowingProjectFilter(filters.BaseFilterBackend):
    """
    Filter projects so that user only sees projects that they are managing, participating in, or subscribed to
    """
    def filter_queryset(self, request, queryset, view):
        following = view.request.query_params.get('following',None)
        if not following:
            return queryset
        clauses = [Q(manager=request.user)]#,Q(participants__id=request.user.id)
        try:
            from notifications.models import UserSubscription
            from django.contrib.contenttypes.models import ContentType
            from glims.models import Project
            ct = ContentType.objects.get_for_model(Project)
            project_ids = UserSubscription.objects.filter(user=request.user,content_type=ct,subscribed=True).values_list('object_id',flat=True)
            print project_ids
            clauses.append(Q(id__in=[int(id) for id in project_ids])) 
        except Exception, e:
            print e.message
            pass
        print 'filtering'
        query = reduce(operator.or_,clauses)
#         print query
        queryset =  queryset.filter(query)
#         print queryset.query
        return queryset 