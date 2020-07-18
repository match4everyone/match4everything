from rest_framework.pagination import LimitOffsetPagination


class StrictLimitOffsetPagination(LimitOffsetPagination):
    max_limit = 15
