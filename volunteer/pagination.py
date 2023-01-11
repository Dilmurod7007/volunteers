from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size_query_param = "size"
    page_size = 8

    def get_paginated_response(self, data):
        return Response(
            {
                "page_size": self.get_page_size(self.request),
                "current_page": self.page.number,
                "total_pages": self.page.paginator.num_pages,
                "page_items": len(self.page),
                "total": self.page.paginator.count,
                "results": data,
            }, status=status.HTTP_200_OK
        )


class EventVolunteersPagination(PageNumberPagination):
    page_size = 8

