from django.contrib.auth.models import Group, User
from rest_framework import serializers

from api.models import Anexo


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class AnexoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anexo
        fields = ['id','nome', 'data','arquivo']