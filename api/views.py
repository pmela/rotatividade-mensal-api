from django.shortcuts import render
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets

from api.models import Anexo
from api.serializers import UserSerializer, AnexoSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class AnexoViewSet(viewsets.ModelViewSet):
    queryset = Anexo.objects.all().order_by('-data')
    serializer_class = AnexoSerializer
    permission_classes = []
