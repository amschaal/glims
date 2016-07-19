from rest_framework.pagination import PageNumberPagination
class StandardPagePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000
    
# class FileBrowserPagination(StandardPagePagination):
#     page_size = 10
#     page_size_query_param = 'page_size'
#     max_page_size = 1000
#     def paginate_queryset(self, queryset, request, view=None):
#         """
#         Paginate a queryset if required, either returning a
#         page object, or `None` if pagination is not configured for this view.
#         """
#         page_size = self.get_page_size(request)
#         if not page_size:
#             return None
# 
#         paginator = self.django_paginator_class(queryset, page_size)
#         page_number = request.query_params.get(self.page_query_param, 1)
#         if page_number in self.last_page_strings:
#             page_number = paginator.num_pages
# 
#         try:
#             self.page = paginator.page(page_number)
#         except InvalidPage as exc:
#             msg = self.invalid_page_message.format(
#                 page_number=page_number, message=six.text_type(exc)
#             )
#             raise NotFound(msg)
# 
#         if paginator.num_pages > 1 and self.template is not None:
#             # The browsable API should display pagination controls.
#             self.display_page_controls = True
# 
#         self.request = request
#         return list(self.page)
#     