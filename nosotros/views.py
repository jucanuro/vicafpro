from rest_framework import generics
from .models import Nosotros
from .serializers import NosotrosSerializer

class NosotrosListView(generics.ListCreateAPIView):
    queryset = Nosotros.objects.all()
    serializer_class = NosotrosSerializer

class NosotrosCreateView(generics.CreateAPIView):
    queryset = Nosotros.objects.all()
    serializer_class = NosotrosSerializer

class NosotrosUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Nosotros.objects.all()
    serializer_class = NosotrosSerializer

class NosotrosDeleteView(generics.DestroyAPIView):
    queryset = Nosotros.objects.all()
    serializer_class = NosotrosSerializer
