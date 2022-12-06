from .models import Category
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.status import HTTP_204_NO_CONTENT
from .serializers import CategorySerializer


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    


# raise 는 실행후 그 뒤의 코드를 실행하지 못하게 함


# """
# serialize translate ptython object(queryset) to JSON also,
# serializer translate JSON that user send to me data to PYthon object that we will put in database
# """
