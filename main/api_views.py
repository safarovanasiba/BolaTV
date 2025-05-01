from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.core.cache import cache

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
    queryset = Ertaklar.objects.all().order_by('order')
    serializer_class = ErtaklarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Optimize queryset with caching"""
        queryset = cache.get('ertaklar_queryset')
        if queryset is None:
            queryset = Ertaklar.objects.all().order_by('order')
            cache.set('ertaklar_queryset', queryset, 300)  # Cache for 5 minutes
        return queryset

class MultfilmlarViewSet(viewsets.ModelViewSet):
    queryset = Multfilmlar.objects.all().order_by('order')
    serializer_class = MultfilmlarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Optimize queryset with caching"""
        queryset = cache.get('multfilmlar_queryset')
        if queryset is None:
            queryset = Multfilmlar.objects.all().order_by('order')
            cache.set('multfilmlar_queryset', queryset, 300)
        return queryset

class QoshiqlarViewSet(viewsets.ModelViewSet):
    queryset = Qoshiqlar.objects.all().order_by('order')
    serializer_class = QoshiqlarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Optimize queryset with caching"""
        queryset = cache.get('qoshiqlar_queryset')
        if queryset is None:
            queryset = Qoshiqlar.objects.all().order_by('order')
            cache.set('qoshiqlar_queryset', queryset, 300)
        return queryset

class QiziqariMatematikaViewSet(viewsets.ModelViewSet):
    queryset = Qiziqari_Matematika.objects.all().order_by('order')
    serializer_class = QiziqariMatematikaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Optimize queryset with caching"""
        queryset = cache.get('qiziqari_matematika_queryset')
        if queryset is None:
            queryset = Qiziqari_Matematika.objects.all().order_by('order')
            cache.set('qiziqari_matematika_queryset', queryset, 300)
        return queryset

class IngliztiliViewSet(viewsets.ModelViewSet):
    queryset = Ingliztili.objects.all().order_by('order')
    serializer_class = IngliztiliSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Optimize queryset with caching"""
        queryset = cache.get('ingliztili_queryset')
        if queryset is None:
            queryset = Ingliztili.objects.all().order_by('order')
            cache.set('ingliztili_queryset', queryset, 300)
        return queryset

class BadantarbiyaViewSet(viewsets.ModelViewSet):
    queryset = Badantarbiya.objects.all().order_by('order')
    serializer_class = BadantarbiyaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Optimize queryset with caching"""
        queryset = cache.get('badantarbiya_queryset')
        if queryset is None:
            queryset = Badantarbiya.objects.all().order_by('order')
            cache.set('badantarbiya_queryset', queryset, 300)
        return queryset

class RasmlarViewSet(viewsets.ModelViewSet):
    queryset = Rasmlar.objects.all().order_by('order')
    serializer_class = RasmlarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Optimize queryset with caching"""
        queryset = cache.get('rasmlar_queryset')
        if queryset is None:
            queryset = Rasmlar.objects.all().order_by('order')
            cache.set('rasmlar_queryset', queryset, 300)
        return queryset

# Ariza viewset
class ArizaViewSet(viewsets.ModelViewSet):
    queryset = Ariza.objects.all()
    serializer_class = ArizaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Optimize queryset with caching"""
        queryset = cache.get('ariza_queryset')
        if queryset is None:
            queryset = Ariza.objects.all()
            cache.set('ariza_queryset', queryset, 300)
        return queryset

# Test viewsets
class TestQuestionViewSet(viewsets.ModelViewSet):
    queryset = TestQuestion.objects.all()
    serializer_class = TestQuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Optimize queryset with caching"""
        queryset = cache.get('test_question_queryset')
        if queryset is None:
            queryset = TestQuestion.objects.all()
            cache.set('test_question_queryset', queryset, 300)
        return queryset

class TestResultViewSet(viewsets.ModelViewSet):
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Optimize queryset with caching"""
        queryset = cache.get('test_result_queryset')
        if queryset is None:
            queryset = TestResult.objects.all()
            cache.set('test_result_queryset', queryset, 300)
        return queryset

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
