import logging

from rest_framework import viewsets

from .serializers import CourseSerializer

logger = logging.getLogger(__name__)


class CourseViewset(viewsets.ModelViewSet):
    queryset = CourseSerializer.Meta.model.objects.all()
    serializer_class = CourseSerializer
