"""Implementa a busca por diários oficiais."""

import logging
import pprint
import re

import html
import requests
from django.conf import settings
from django.core import mail
from email import encoders
from email.mime import base

logger = logging.getLogger(__name__)


class BuscadorDiários:
    """Baixa diários oficiais a partir de uma consulta."""

    def __init__(self):
        """Init."""
        self.parâmetros_busca = {
            'edicao.paginaAtual': '1',
            'edicao.jornal_hidden': '',
            'edicao.fonetica': 'null',
            'edicao.tipoPesquisa': 'pesquisa_avancada',
            'edicao.jornal': '1,1000,1010,1020,2,2000,3,3000,3020,',
            'edicao.fonetica': 'null',
        }

    def obter_urls(self, parâmetros):
        """Obtém urls de diários a partir de parâmetros de busca."""
        # 'parâmetros' é um mapa para sobrescrever termos da busca.
        logger.debug('Obtendo urls de busca...')

        self.parâmetros_busca.update(**parâmetros)
        logger.debug('Parâmetros de busca:\n%s', pprint.pformat(self.parâmetros_busca))

        url_pesquisa = 'http://pesquisa.in.gov.br/imprensa/core/consulta.action'
        página_resultados = requests.post(url_pesquisa, self.parâmetros_busca)

        padrão_url = re.compile(r"href='\.\./jsp/visualiza/index.jsp\?(.+)'")
        query_strings = padrão_url.findall(página_resultados.text)

        template_url_diário = ('http://pesquisa.in.gov.br/imprensa/servlet/INPDFViewer?{}' +
                               '&captchafield=firistAccess')
        urls = [html.unescape(template_url_diário.format(qs)) for qs in query_strings]
        logger.debug('Encontrada(s) %d url(s)', len(urls))
        return urls

    def download(self, urls):
        """Faz o download de diários oficiais a partir de urls."""
        intervalo = '{0}/{2} - {1}/{2}'.format(
            self.parâmetros_busca['edicao.dtInicio'],
            self.parâmetros_busca['edicao.dtFim'],
            self.parâmetros_busca['edicao.ano'],
        )
        subject = 'Oi Igor! Nenhum diario foi encontrado nesse intervalo ({}) a partir da busca '
        subject += '"{}" :/. Amanhã procuro novamente!'
        subject = subject.format(intervalo, self.parâmetros_busca['edicao.txtPesquisa'])

        email = mail.EmailMessage(
            'Consulta Diário {}'.format(intervalo),
            subject,
            'doubot@herokuapp.com',
            [manager[-1] for manager in settings.MANAGERS]
        )
        for index, url in enumerate(urls):
            if index == 0:
                email.body = 'Oi Igor! Foram encontrados diários nesse intervalo ({}) a partir da'
                email.body += ' busca "{}"! :D. Segue em anexo:'
                email.body = email.body.format(intervalo, self.parâmetros_busca['edicao.txtPesquisa'])

            logger.info('Baixando diário a partir da url %s', url)

            diário_pdf = requests.get(url).content

            attachment = base.MIMEBase('application', 'pdf')
            attachment.set_payload(diário_pdf)
            encoders.encode_base64(attachment)

            nome_arquivo = '{}-{}'.format(
                self.parâmetros_busca['edicao.dtInicio'],
                self.parâmetros_busca['edicao.dtFim']
            )
            nome_arquivo = '[{}][{}]({}).pdf'.format(
                self.parâmetros_busca['edicao.txtPesquisa'],
                nome_arquivo,
                index
            ).replace('/', '.')
            attachment.add_header('Content-Disposition', 'attachment', filename=nome_arquivo)

            email.attach(attachment)

        email.send()

    def salvar_diários(self, opções):
        """Salva diários resultantes da pesquisa solicitada."""
        parâmetros = self._construir_paramêtros_busca(opções)
        urls = self.obter_urls(parâmetros)
        self.download(urls)

    def _construir_paramêtros_busca(self, opções):
        """Controe um mapa de parâmetros a partir de um objeto opções."""
        return {
            'edicao.txtPesquisa': opções['pesquisa'],
            'edicao.dtInicio': opções['data_inicial'],
            'edicao.dtFim': opções['data_final'],
            'edicao.ano': opções['ano'],
        }
