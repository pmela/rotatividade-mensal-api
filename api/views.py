from django.contrib.auth.models import User
from rest_framework import permissions, viewsets

from api.models import Anexo
from api.serializers import UserSerializer, AnexoSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response

import os
import pandas as pd
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


@api_view(['POST'])
def analise(request):
    id = request.data['id']
    anexo = Anexo.objects.get(id=id)
    tipo_arquivo = os.path.splitext(anexo.arquivo.name)[1]
    if tipo_arquivo == '.xlsx':
        df = pd.read_excel(anexo.arquivo)
    elif tipo_arquivo == '.csv':
        df = pd.read_csv(anexo.arquivo)
    else:
        return Response({'mensagem': 'Formato de arquivo inválido'})

    canceladas_boolean = df['status'] == 'Cancelada'
    planilha_cancelamentos = df[canceladas_boolean]
    quantidade_cancelados = len(planilha_cancelamentos)

    grafico = [
        {'mes': 'Janeiro', 'cancelados': 0, 'novos': 0, 'percentual': 0},
        {'mes': 'Fevereiro', 'cancelados': 0, 'novos': 0, 'percentual': 0},
        {'mes': 'Março', 'cancelados': 0, 'novos': 0, 'percentual': 0},
        {'mes': 'Abril', 'cancelados': 0, 'novos': 0, 'percentual': 0},
        {'mes': 'Maio', 'cancelados': 0, 'novos': 0, 'percentual': 0},
        {'mes': 'Junho', 'cancelados': 0, 'novos': 0, 'percentual': 0},
        {'mes': 'Julho', 'cancelados': 0, 'novos': 0, 'percentual': 0},
        {'mes': 'Agosto', 'cancelados': 0, 'novos': 0, 'percentual': 0},
        {'mes': 'Setembro', 'cancelados': 0, 'novos': 0, 'percentual': 0},
        {'mes': 'Outubro', 'cancelados': 0, 'novos': 0, 'percentual': 0},
        {'mes': 'Novembro', 'cancelados': 0, 'novos': 0, 'percentual': 0},
        {'mes': 'Dezembro', 'cancelados': 0, 'novos': 0, 'percentual': 0}
    ]

    for linha in df.values:
        if type(linha[2]) == str:
            data_inicio = datetime.datetime.strptime(linha[2], '%m/%d/%y %H:%M')
        else:
            data_inicio = linha[2]
        if data_inicio.year == 2022:
            grafico[data_inicio.month - 1]['novos'] += 1
        if linha[3] == 'Cancelada':
            if type(linha[5]) == str:
                data_cancelamento = datetime.datetime.strptime(linha[5], '%m/%d/%y %H:%M')
            else:
                data_cancelamento = linha[5]
            grafico[data_cancelamento.month - 1]['cancelados'] += 1

    for linha_grafico in grafico:
        if linha_grafico['cancelados'] is not 0:
            linha_grafico['percentual'] = linha_grafico['cancelados'] / linha_grafico['novos'] * 100

    mes_mais_cancelado = {'mes': '', 'cancelados': 0, 'novos': 0, 'percentual': 0}
    for x in grafico:
        if mes_mais_cancelado.get('cancelados') < x.get('cancelados'):
            mes_mais_cancelado = x

    mes_menos_cancelado = {'mes': '', 'cancelados': mes_mais_cancelado.get('cancelados'), 'novos': 0, 'percentual': 0}
    for x in grafico:
        if mes_menos_cancelado.get('cancelados') > x.get('cancelados'):
            mes_menos_cancelado = x


    ativa_boolean = df['status'] == 'Ativa'
    planilha_ativa = df[ativa_boolean]
    quantidade_ativos = len(planilha_ativa)

    antigo_ativo = planilha_ativa.values[1]
    for linha in planilha_ativa.values:
        if type(linha[2]) == str:
            data_convertida = datetime.datetime.strptime(linha[2], '%m/%d/%y %H:%M')
        else:
            data_convertida = linha[2]
        if type(antigo_ativo[2]) == str:
            antigo_ativo_convertida = datetime.datetime.strptime(antigo_ativo[2], '%m/%d/%y %H:%M')
        else:
            antigo_ativo_convertida = antigo_ativo[2]

        if data_convertida < antigo_ativo_convertida:
            antigo_ativo = linha


    atrasada = df['status'] == 'Atrasada'
    planilha_atrasada = df[atrasada]
    total_atrasados = len(planilha_atrasada)

    trial = df['status'] == 'Trial cancelado'
    planilha_trial = df[trial]
    total_trial = len(planilha_trial)

    contexto = {
        'total_trial': total_trial,
        'total_atrasados': total_atrasados,
        'antigo_ativo': antigo_ativo[8],
        'quantidade_ativos': quantidade_ativos,
        'mes_menos_cancelado': mes_menos_cancelado,
        'mes_mais_cancelado': mes_mais_cancelado,
        'quantidade_cancelados': quantidade_cancelados,
        'grafico': grafico,
    }

    return Response(contexto)
