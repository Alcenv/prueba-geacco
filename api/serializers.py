from rest_framework import serializers
from .models import Documento, Tarea, SecuenciaTarea
from django.contrib.auth.models import User


class DocumentoSerializer(serializers.ModelSerializer):
    formato = serializers.ChoiceField(choices=[('txt', 'Texto'), ('docx', 'DOCX'), ('xlsx', 'XLSX')])
    class Meta:
        model = Documento
        fields = ['nombre', 'placa', 'entidad', 'formato']

class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

class SecuenciaTareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecuenciaTarea
        fields = '__all__'