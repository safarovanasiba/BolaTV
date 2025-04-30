from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

from .models import (
    Ertaklar, Multfilmlar, Qoshiqlar, Qiziqari_Matematika, 
    Ingliztili, Badantarbiya, Rasmlar, Ariza, TestQuestion, TestResult
)
from .serializers import (
    ErtaklarSerializer, MultfilmlarSerializer, QoshiqlarSerializer, 
    QiziqariMatematikaSerializer, IngliztiliSerializer, BadantarbiyaSerializer, 
    RasmlarSerializer, ArizaSerializer, TestQuestionSerializer, TestResultSerializer
)

# Video categories viewsets
class ErtaklarViewSet(viewsets.ModelViewSet):
    queryset = Ertaklar.objects.all()
    serializer_class = ErtaklarSerializer
    permission_classes = [permissions.AllowAny]

class MultfilmlarViewSet(viewsets.ModelViewSet):
    queryset = Multfilmlar.objects.all()
    serializer_class = MultfilmlarSerializer
    permission_classes = [permissions.AllowAny]

class QoshiqlarViewSet(viewsets.ModelViewSet):
    queryset = Qoshiqlar.objects.all()
    serializer_class = QoshiqlarSerializer
    permission_classes = [permissions.AllowAny]

class QiziqariMatematikaViewSet(viewsets.ModelViewSet):
    queryset = Qiziqari_Matematika.objects.all()
    serializer_class = QiziqariMatematikaSerializer
    permission_classes = [permissions.AllowAny]

class IngliztiliViewSet(viewsets.ModelViewSet):
    queryset = Ingliztili.objects.all()
    serializer_class = IngliztiliSerializer
    permission_classes = [permissions.AllowAny]

class BadantarbiyaViewSet(viewsets.ModelViewSet):
    queryset = Badantarbiya.objects.all()
    serializer_class = BadantarbiyaSerializer
    permission_classes = [permissions.AllowAny]

class RasmlarViewSet(viewsets.ModelViewSet):
    queryset = Rasmlar.objects.all()
    serializer_class = RasmlarSerializer
    permission_classes = [permissions.AllowAny]

# Ariza viewset
class ArizaViewSet(viewsets.ModelViewSet):
    queryset = Ariza.objects.all()
    serializer_class = ArizaSerializer
    permission_classes = [permissions.AllowAny]

# Test viewsets
class TestQuestionViewSet(viewsets.ModelViewSet):
    queryset = TestQuestion.objects.all()
    serializer_class = TestQuestionSerializer
    permission_classes = [permissions.AllowAny]

class TestResultViewSet(viewsets.ModelViewSet):
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer
    permission_classes = [permissions.AllowAny]

@api_view(['GET'])
def api_root(request):
    """
    API root endpoint showing available endpoints
    """
    return Response({
        'ertaklar': 'api/ertaklar/',
        'multfilmlar': 'api/multfilmlar/',
        'qoshiqlar': 'api/qoshiqlar/',
        'matematika': 'api/matematika/',
        'ingliztili': 'api/ingliztili/',
        'badantarbiya': 'api/badantarbiya/',
        'rasmlar': 'api/rasmlar/',
        'ariza': 'api/ariza/',
        'test-questions': 'api/test-questions/',
        'test-results': 'api/test-results/',
    })
