# proyectos/api_views.py

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Importamos todos los modelos
from .models import Proyecto, OrdenDeEnsayo, Muestra, ResultadoEnsayo, DocumentoFinal, Servicio

# Importamos todos los serializadores nuevos
from .serializers import (
    ProyectoSerializer,
    OrdenDeEnsayoSerializer,
    MuestraSerializer,
    ResultadoEnsayoSerializer,
    DocumentoFinalSerializer,
    ServicioSerializer,
)

# ================================================================
#  ViewSets para el API
# ================================================================

class ProyectoViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite visualizar o editar proyectos.
    Proporciona automáticamente las operaciones CRUD:
    - GET /api/proyectos/ (Listar)
    - POST /api/proyectos/ (Crear)
    - GET /api/proyectos/{id}/ (Recuperar por ID)
    - PUT /api/proyectos/{id}/ (Actualizar por ID)
    - PATCH /api/proyectos/{id}/ (Actualización parcial)
    - DELETE /api/proyectos/{id}/ (Eliminar por ID)
    
    Permite filtrar por estado del proyecto usando un parámetro de consulta `estado`.
    Ejemplo: /api/proyectos/?estado=FINALIZADO
    """
    serializer_class = ProyectoSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """
        Sobrescribe el queryset para permitir el filtrado por estado.
        """
        queryset = Proyecto.objects.all().order_by('-creado_en')
        estado = self.request.query_params.get('estado', None)
        
        if estado is not None:
            # Asegúrate de que el estado coincida con las opciones del modelo
            queryset = queryset.filter(estado=estado.upper()) 
            
        return queryset

    def update(self, request, *args, **kwargs):
        # 1. Obtener la instancia del proyecto antes de la actualización
        instance = self.get_object()
        old_estado = instance.estado

        # 2. Actualizar el proyecto con los datos de la solicitud
        response = super().update(request, *args, **kwargs)
        
        # 3. Obtener la instancia actualizada para verificar el nuevo estado
        updated_instance = self.get_object()
        new_estado = updated_instance.estado

        # 4. Verificar si el estado cambió a 'FINALIZADO' y no había sido notificado antes
        if new_estado == 'FINALIZADO' and old_estado != 'FINALIZADO' and not updated_instance.notificado_cliente:
            self.enviar_notificacion_finalizacion(updated_instance)
            
            # Actualizar el campo notificado_cliente y guardar el cambio
            updated_instance.notificado_cliente = True
            updated_instance.save(update_fields=['notificado_cliente'])

            # 5. Volver a generar la respuesta JSON para que refleje todos los cambios
            return self.retrieve(request, *args, **kwargs)
            
        return response

    def enviar_notificacion_finalizacion(self, proyecto):
        """
        Función para enviar un correo de notificación al cliente.
        """
        if proyecto.cliente and proyecto.cliente.correo_contacto:
            asunto = f"Vicafpro: El proyecto '{proyecto.nombre_proyecto}' ha finalizado"
            
            html_message = f"""
            <html>
                <body>
                    <p>Estimado/a {proyecto.cliente.razon_social if proyecto.cliente.razon_social else 'cliente'},</p>
                    <p>Le escribimos para informarle que el proyecto <b>{proyecto.nombre_proyecto}</b> ha sido marcado como finalizado.</p>
                    <p>Sus resultados ya están disponibles. Por favor, acceda a su portal para revisarlos.</p>
                    <p>Gracias por confiar en Vicafpro.</p>
                </body>
            </html>
            """
            plain_message = strip_tags(html_message)
            from_email = 'adm.vicaf@gmail.com' # Correo desde el que se envía
            to_email = [proyecto.cliente.correo_contacto]

            try:
                send_mail(
                    asunto,
                    plain_message,
                    from_email,
                    to_email,
                    html_message=html_message,
                )
                print(f"Correo de finalización enviado al cliente {proyecto.cliente.razon_social}")
            except Exception as e:
                print(f"Error al enviar el correo: {e}")

class OrdenDeEnsayoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para órdenes de ensayo.
    """
    queryset = OrdenDeEnsayo.objects.all()
    serializer_class = OrdenDeEnsayoSerializer
    permission_classes = [permissions.AllowAny]

class MuestraViewSet(viewsets.ModelViewSet):
    """
    API endpoint para muestras.
    """
    queryset = Muestra.objects.all()
    serializer_class = MuestraSerializer
    permission_classes = [permissions.AllowAny]

class ResultadoEnsayoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para resultados de ensayos.
    """
    queryset = ResultadoEnsayo.objects.all().order_by('-fecha_realizacion')
    serializer_class = ResultadoEnsayoSerializer
    permission_classes = [permissions.AllowAny]

class DocumentoFinalViewSet(viewsets.ModelViewSet):
    """
    API endpoint para documentos finales.
    """
    queryset = DocumentoFinal.objects.all().order_by('-fecha_emision')
    serializer_class = DocumentoFinalSerializer
    permission_classes = [permissions.AllowAny]

class ServicioViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite visualizar o editar servicios.
    """
    queryset = Servicio.objects.all().order_by('orden')
    serializer_class = ServicioSerializer
    permission_classes = [permissions.AllowAny]

