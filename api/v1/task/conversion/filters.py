from api.v1.task.filters import TaskFilter, CharInFilter


class ConversionTaskFilter(TaskFilter):
    media_type = CharInFilter(field_name="upload__media_type", lookup_expr="in")
