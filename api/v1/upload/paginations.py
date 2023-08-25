from rest_framework.pagination import PageNumberPagination


class UploadPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100
