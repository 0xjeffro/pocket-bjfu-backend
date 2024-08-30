from rest_framework.pagination import PageNumberPagination


class ContentPagination(PageNumberPagination):
    page_size = 14
    max_page_size = 10000

