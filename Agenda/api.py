from rest_framework import permissions, routers, viewsets

from .models import Contacto
from .serializers import ContactoSerializer


class ContactoViewSet(viewsets.ModelViewSet):
    queryset = Contacto.objects.all()
    serializer_class = ContactoSerializer
    permission_classes = [permissions.IsAuthenticated]


router = routers.DefaultRouter()
router.register(r'contactos', ContactoViewSet)