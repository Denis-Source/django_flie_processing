from drf_yasg.utils import swagger_auto_schema

from api.v1.task.document.serializers import DocumentConversionTaskSerializer
from api.v1.task.views import GenericRetrieveFormatsView, CreateConversionTaskView, \
    RetrieveConversionTaskView
from task.document.constants import INPUT_FORMATS, OUTPUT_FORMATS
from task.document.tasks import convert_document
from task.models import DocumentConversionTask


class RetrieveDocumentFormatsView(GenericRetrieveFormatsView):
    input_formats = INPUT_FORMATS
    output_formats = OUTPUT_FORMATS

    @swagger_auto_schema(
        tags=["Document"],
        responses={
            200: "Dictionary of all available formats and their names"})
    def get(self, request, *args, **kwargs):
        """Retrieve a list of available input and output formats"""
        return super().get(request, *args, **kwargs)


class CreateDocumentConversionTaskView(CreateConversionTaskView):
    model_class = DocumentConversionTask
    serializer_class = DocumentConversionTaskSerializer
    celery_task = convert_document

    @swagger_auto_schema(
        tags=["Document"],
        responses={
            201: DocumentConversionTaskSerializer,
            400: "Bad request",
            401: "Unauthorized"})
    def post(self, request, *args, **kwargs):
        """
        Create document conversion task

        Response does not contain a converted result,
        but contains task id to retrieve a result if the future"""
        return super().post(request, *args, **kwargs)


class RetrieveDocumentConversionTaskView(RetrieveConversionTaskView):
    serializer_class = DocumentConversionTaskSerializer
    model_class = DocumentConversionTask

    @swagger_auto_schema(
        tags=["Document"],
        responses={
            200: DocumentConversionTaskSerializer,
            401: "Unauthorized"})
    def get(self, request, *args, **kwargs):
        """
        Retrieve document conversion task

        Task could not contain a result as it will not necessary will be finished
        """
        return super().get(request, *args, **kwargs)
