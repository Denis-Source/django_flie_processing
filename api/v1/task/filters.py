from django_filters import FilterSet, CharFilter, BaseInFilter, OrderingFilter


class CharInFilter(BaseInFilter, CharFilter):
    pass


class TaskFilter(FilterSet):
    status = CharInFilter(field_name="status", lookup_expr="in")
    ordering = OrderingFilter(
        fields=(
            ("created_at", "created_at"),
            ("closed_at", "closed_at"),
            ("status", "status"),
            ("name", "name")
        ),
    )