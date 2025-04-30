from rest_framework import serializers
from .models import (
    Ertaklar, Multfilmlar, Qoshiqlar, Qiziqari_Matematika, 
    Ingliztili, Badantarbiya, Rasmlar, Ariza, TestQuestion, TestResult
)

class ErtaklarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ertaklar
        fields = '__all__'

class MultfilmlarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Multfilmlar
        fields = '__all__'

class QoshiqlarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qoshiqlar
        fields = '__all__'

class QiziqariMatematikaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qiziqari_Matematika
        fields = '__all__'

class IngliztiliSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingliztili
        fields = '__all__'

class BadantarbiyaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badantarbiya
        fields = '__all__'

class RasmlarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rasmlar
        fields = '__all__'

class ArizaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ariza
        fields = '__all__'

class TestQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestQuestion
        fields = '__all__'

class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = '__all__'
