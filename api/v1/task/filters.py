from django_filters import FilterSet, CharFilter, BaseInFilter, OrderingFilter


class CharInFilter(BaseInFilter, CharFilter):
    pass

class CaseInsensitivePartialMatchCharFilter(CharFilter):
    def filter(self, qs, value):
        if value:
            self.lookup_expr = "icontains"
        return super().filter(qs, value)

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
    name = CaseInsensitivePartialMatchCharFilter(field_name="name")
