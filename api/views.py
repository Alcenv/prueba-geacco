from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Documento, Tarea, SecuenciaTarea
from .serializers import DocumentoSerializer, TareaSerializer, UserSerializer, SecuenciaTareaSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from django_celery_beat.models import PeriodicTask, IntervalSchedule


class GenerarDocumentoView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = DocumentoSerializer(data=data)
        if serializer.is_valid():
            documento = Documento(**serializer.validated_data)
            documento.save()

            if documento.formato == 'txt':
                print("Llamando al método generar_documento_txt()...")
                file_path = documento.generar_documento_txt()
                if file_path is not None:
                    with open(file_path, 'r') as file:
                        response = HttpResponse(file.read(), content_type='text/plain')
                        response['Content-Disposition'] = f'attachment; filename="{documento.nombre}.txt"'
                    return response
            elif documento.formato == 'docx':
                print("Llamando al método generar_documento_docx()...")
                file_path = documento.generar_documento_docx()
                if file_path is not None:
                    with open(file_path, 'rb') as file:
                        response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                        response['Content-Disposition'] = f'attachment; filename="{documento.nombre}.docx"'
                    return response
            elif documento.formato == 'xlsx':
                print("Llamando al método generar_documento_xlsx()...")
                file_path = documento.generar_documento_xlsx()
                if file_path is not None:
                    with open(file_path, 'rb') as file:
                        response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                        response['Content-Disposition'] = f'attachment; filename="{documento.nombre}.xlsx"'
                    return response
        return Response(serializer.errors, status=400)


class ConfigurarTareaView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = TareaSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        documento_id = data.get('documento')
        if documento_id is None:
            return Response({'message': 'ID del documento no proporcionado'}, status=400)

        try:
            documento = Documento.objects.get(id=documento_id)
        except Documento.DoesNotExist:
            return Response({'message': 'El documento seleccionado no existe'}, status=400)

        if documento.entregado:
            return Response({'message': 'El documento ya ha sido entregado'}, status=400)

        tarea = Tarea(**serializer.validated_data)
        tarea.documento = documento
        tarea.save()
            
        # Crear una tarea periódica para generar el documento
        schedule, _ = IntervalSchedule.objects.get_or_create(
            every=data.get('intervalo', 2),  # Usar el intervalo proporcionado por el usuario, o 2 días por defecto
            period=IntervalSchedule.MINUTES,
        )
        task_name = f'Generar documento {documento.id}'
            
        # Intenta obtener la tarea con ese nombre
        try:
            task = PeriodicTask.objects.get(name=task_name)
            # Si la tarea ya existe, actualiza los argumentos y el intervalo
            task.args = str([documento.id])
            task.interval = schedule
            task.save()
        except PeriodicTask.DoesNotExist:
            # Si la tarea no existe, créala
            PeriodicTask.objects.create(
                interval=schedule,
                name=task_name,
                task='api.models.generar_documento_task',
                args=str([documento.id]),
            )
        return Response({'message': 'Tarea programada correctamente'})
    

    
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'user_id': token.user_id})

class CreateUserView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            email = serializer.validated_data['email']

            # Crea el usuario en la base de datos
            user = User.objects.create_user(username=username, password=password, email=email)

            # Devuelve la respuesta de éxito
            return Response({'message': 'Usuario creado exitosamente'})
        else:
            # Devuelve los errores de validación en caso de que los haya
            return Response(serializer.errors, status=400)
        
class SecuenciaTareaViewSet(viewsets.ModelViewSet):
    queryset = SecuenciaTarea.objects.all()
    serializer_class = SecuenciaTareaSerializer