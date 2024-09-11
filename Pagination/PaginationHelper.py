from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import status
from rest_framework.response import Response


class PaginationHelper:
    def __init__(self, data, page_size, page):
        self.data = data
        self.page_size = page_size
        self.page = page

    def paginate(self):
        paginator = Paginator(self.data, self.page_size)
        try:
            paginated_data = paginator.page(self.page)
        except PageNotAnInteger:
            return Response({"error": "Invalid page number. It must be an integer."},
                            status=status.HTTP_400_BAD_REQUEST)
        except EmptyPage:
            return Response({"error": "Page number out of range. It must be between 1 and the total number of pages."},
                            status=status.HTTP_400_BAD_REQUEST)
        return paginated_data.object_list

    @staticmethod
    def validate_params(page_size, page):
        try:
            page_size = int(page_size)
            if page_size <= 0:
                return False, "Invalid page_size. It must be a positive integer."
        except ValueError:
            return False, "Invalid page_size. It must be an integer."

        try:
            page = int(page)
            if page <= 0:
                return False, "Invalid page. It must be a positive integer."
        except ValueError:
            return False, "Invalid page. It must be an integer."

        return True, ""
