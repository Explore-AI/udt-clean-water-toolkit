from rest_framework import pagination
from rest_framework.response import Response
from config.settings import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE


class BasePagination(pagination.PageNumberPagination):
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = "page_size"
    max_page_size = MAX_PAGE_SIZE

    def get_paginated_response(self, data):

        page_size = self.get_page_size(self.request)

        first_item_index = ((page_size * self.page.number) - page_size) + 1
        last_item_index = page_size * self.page.number

        if page_size:
            response_pagination = {
                "next_page": self.page.next_page_number()
                if self.page.has_next()
                else None,
                "current_page": self.page.number,
                "prev_page": self.page.previous_page_number()
                if self.page.has_previous()
                else None,
                "page_size": page_size,
                "num_items": self.page.paginator.count,
                "num_pages": self.page.paginator.num_pages,
                "first_item_index": first_item_index,
                "last_item_index": last_item_index,
            }
            return Response({"pagination": response_pagination, "items": data})

        return Response({"items": data})
