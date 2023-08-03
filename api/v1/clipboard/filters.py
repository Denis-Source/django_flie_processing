from django_filters import FilterSet, CharFilter, BaseInFilter, OrderingFilter


class CharInFilter(BaseInFilter, CharFilter):
    pass


class ClipBoardFilter(FilterSet):
    status = CharInFilter(field_name="media_type", lookup_expr="in")
    ordering = OrderingFilter(
        fields=(
            ("auto_delete", "auto_delete"),
            ("created_at", "created_at"),
            ("media_type", "media_type"),
            ("name", "name")
        ),
    )
