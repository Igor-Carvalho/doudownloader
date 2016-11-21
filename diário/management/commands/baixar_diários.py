"""Comando para fazer o download de diários oficiais."""

import datetime

from django.core.management import base

from ... import busca


class Command(base.BaseCommand):
    """Comando."""

    def add_arguments(self, parser):
        """Adiciona opções da linha de comando."""
        parser.add_argument('--log', default='info')

        dia_mês = datetime.date.today().strftime('%d/%m')

        start_date_options = dict(
            metavar='Data inicial da busca', default=dia_mês, dest='data_inicial', help="ex: 23/11"
        )
        parser.add_argument('--data-inicial', **start_date_options)

        end_date_options = dict(
            metavar='Data final da busca', default=dia_mês, dest='data_final', help="ex: 22/10"
        )
        parser.add_argument('--data-final', **end_date_options)

        parser.add_argument('--ano', default=datetime.date.today().strftime('%Y'))
        parser.add_argument('--pesquisa', default='igor+barbosa')

    def handle(self, *args, **options):
        """Executa o comando."""
        busca.BuscadorDiários().salvar_diários(options)
