"""Módulo que contém as tarefas locais utilizadas com invoke."""

import invoke


@invoke.task
def makemigrations(ctx, settings='development'):
    """Gera os arquivos de migração."""
    cmd = './manage.py makemigrations --settings=doubot.settings.{}'.format(settings)
    ctx.run(cmd, echo=True, pty=True)


@invoke.task
def migrate(ctx, settings='development'):
    """Aplica as migrações."""
    cmd = './manage.py migrate --settings=doubot.settings.{}'.format(settings)
    ctx.run(cmd, echo=True, pty=True)


@invoke.task
def test(ctx, tests='', settings='test'):
    """Testa as aplicações do projeto (com exceção dos testes funcionais)."""
    cmd = 'coverage run ./manage.py test {} --settings=doubot.settings.{}'.format(tests, settings)
    ctx.run(cmd, echo=True, pty=True)
    cmd = 'coverage report'
    ctx.run(cmd, echo=True, pty=True)


@invoke.task(default=True)
def run_server(ctx, settings='development'):
    """Executa o servidor web de desenvolvimento local."""
    cmd = './manage.py runserver 0.0.0.0:8000 --settings=doubot.settings.{}'.format(settings)
    if 'prod' in settings:
        cmd = 'gunicorn doubot.wsgi --workers=4'

    ctx.run(cmd, echo=True, pty=True)


@invoke.task
def collectstatic(ctx, settings='development', noinput=False, clear=False):
    """Coleta arquivos estáticos."""
    noinput = '--noinput' if noinput else ''
    clear = '--clear' if clear else ''
    cmd = './manage.py collectstatic {} {} --settings=doubot.settings.{}'
    cmd = cmd.format(noinput, clear, settings)
    ctx.run(cmd, echo=True, pty=True)


@invoke.task
def send_queued_mail(ctx, settings='development'):
    """Envia emails enfileirados pela aplicação django_post_office."""
    cmd = './manage.py send_queued_mail --settings=doubot.settings.{}'.format(settings)
    ctx.run(cmd, echo=True, pty=True)
