from django_filters import FilterSet, CharFilter, BaseInFilter, OrderingFilter


class CharInFilter(BaseInFilter, CharFilter):
    pass


class CaseInsensitivePartialMatchCharFilter(CharFilter):
    def filter(self, qs, value):
        if value:
            self.lookup_expr = "icontains"
        return super().filter(qs, value)


class UploadFilter(FilterSet):
    media_type = CharInFilter(field_name="media_type", lookup_expr="in")
    name = CaseInsensitivePartialMatchCharFilter(field_name="name")
    ordering = OrderingFilter(
        fields=(
            ("auto_delete", "auto_delete"),
            ("created_at", "created_at"),
            ("media_type", "media_type"),
            ("name", "name")
        ),
    )
