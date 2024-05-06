from django_filters import rest_framework as filters


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass


class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class BaseFilter(filters.FilterSet):
    ids = NumberInFilter(field_name="id", lookup_expr="in")
    id = filters.CharFilter(field_name="id")
    gid = filters.CharFilter(field_name="gid")
    gids = filters.CharFilter(field_name="gid", lookup_expr="in")
    ordering = filters.CharFilter(method="filter_ordering")

    def filter_ordering(self, qs, name, value):
        field = value.split("__")[0]
        ordering = value.split("__")[1]

        if ordering == "asc":
            qs = qs.order_by(field)
        elif ordering == "dsc":
            qs = qs.order_by(f"-{field}")
        return qs
