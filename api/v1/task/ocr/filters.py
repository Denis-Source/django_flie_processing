from api.v1.task.filters import TaskFilter, CharInFilter


class OCRFilter(TaskFilter):
    language = CharInFilter(field_name="language", lookup_expr="in")
