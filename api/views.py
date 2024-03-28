from django.shortcuts import render
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets

from api.models import Anexo
from api.serializers import UserSerializer, AnexoSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response

import os

import csv
import numpy as np
import pandas as pd
import requests
import datetime

from configuracao import settings


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class AnexoViewSet(viewsets.ModelViewSet):
    queryset = Anexo.objects.all().order_by('-data')
    serializer_class = AnexoSerializer
    permission_classes = []


@api_view()
def planilha(request):
    diretorio = os.path.join(settings.BASE_DIR, 'uploads/planilha/planilha.csv')
    # dentro do abaixo vai as informações se e data, e e dinheiro por , etc
    df = pd.read_csv(diretorio)
    print(df)
    canceladas_boolean = df['status'] == 'Cancelada'
    print(canceladas_boolean)
    planilha_cancelamentos = df[canceladas_boolean]
    print(planilha_cancelamentos)
    quantidade_cancelados = len(planilha_cancelamentos)

    print(planilha_cancelamentos['data cancelamento'])
    datas_cancelamento = planilha_cancelamentos['data cancelamento'].values
    grafico = [
        {'mes_escrito': 'Janeiro', 'total': 0},
        {'mes_escrito': 'Fevereiro', 'total': 0},
        {'mes_escrito': 'Março', 'total': 0},
        {'mes_escrito': 'Abril', 'total': 0},
        {'mes_escrito': 'Maio', 'total': 0},
        {'mes_escrito': 'Junho', 'total': 0},
        {'mes_escrito': 'Julho', 'total': 0},
        {'mes_escrito': 'Agosto', 'total': 0},
        {'mes_escrito': 'Setembro', 'total': 0},
        {'mes_escrito': 'Outubro', 'total': 0},
        {'mes_escrito': 'Novembro', 'total': 0},
        {'mes_escrito': 'Dezembro', 'total': 0}
    ]
    for data in datas_cancelamento:
        data_convertida = datetime.datetime.strptime(data, '%m/%d/%y %H:%M')
        grafico[data_convertida.month - 1]['total'] += 1
        # print(data_convertida)
    print(grafico)

    mes_maior = {'mes_escrito': '', 'total': 0}
    for x in grafico:
        if mes_maior.get('total') < x.get('total'):
            mes_maior = x
    print(mes_maior)

    mes_menor = {'mes_escrito': '', 'total': mes_maior.get('total')}
    for x in grafico:
        if mes_menor.get('total') > x.get('total'):
            mes_menor = x
    print(mes_menor)

    ativa_boolean = df['status'] == 'Ativa'
    print(ativa_boolean)
    planilha_ativa = df[ativa_boolean]
    print(planilha_ativa)
    quantidade_ativos = len(planilha_ativa)

    antigo_ativo = planilha_ativa.values[1]

    for linha in planilha_ativa.values:
        data_convertida = datetime.datetime.strptime(linha[2], '%m/%d/%y %H:%M')
        antigo_ativo_convertida = datetime.datetime.strptime(antigo_ativo[2], '%m/%d/%y %H:%M')

        if data_convertida < antigo_ativo_convertida:
            antigo_ativo = linha

    print(antigo_ativo)
    print(antigo_ativo[8])

    return Response({"message": "Hello, world!"})
