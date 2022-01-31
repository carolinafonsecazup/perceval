import logging
import os

import pygsheets
from dotenv import load_dotenv
from perceval.backends.core.dockerhub import DockerHub

load_dotenv()
"""Configuração de logging"""
logging.basicConfig(level=logging.INFO)

"""Configuração de autorização da api no Google Sheets"""
google = pygsheets.authorize(service_account_env_var=os.environ.get("GDRIVE_API_CREDENTIALS"))

"""Configuração de chamada da planilha específica"""
sheets = google.open_by_key("1fqJlKSYn1IgGD88LdFabPw3psCc8cS1FfZAKLrmx3lk")
logging.info("Conexão com o google sheets feita com sucesso")
"""Configuração da página específica a ser trabalhada"""
worksheet = sheets.worksheet_by_title("dockerhubpulls")

repos = {DockerHub("horuszup", "horusec-cli"),
         DockerHub("horuszup", "horusec-manager"),
         DockerHub("horuszup", "horusec-auth"),
         DockerHub("horuszup", "horusec-core"),
         DockerHub("horuszup", "horusec-api"),
         DockerHub("horuszup", "horusec-analytic"),
         DockerHub("horuszup", "horusec-migration"),
         DockerHub("horuszup", "horusec-vulnerability"),
         DockerHub("horuszup", "horusec-messages"),
         DockerHub("horuszup", "horusec-webhook"),
         DockerHub("zupcharles", "charlescd-keycloak"),
         DockerHub("zupcharles", "charlescd-ui"),
         DockerHub("zupcharles", "charlescd-moove"),
         DockerHub("zupcharles", "charlescd-villager"),
         DockerHub("zupcharles", "charlescd-compass"),
         DockerHub("zupcharles", "charlescd-circle-matcher"),
         DockerHub("zupcharles", "charlescd-butler"),
         DockerHub("zupcharles", "charlescd-gate"),
         DockerHub("zupcharles", "charlescd-hermes"),
         DockerHub("zupcharles", "charlescd-octopipe"),
         DockerHub("ritclizup", "rit-python3-pyinstaller-runner"),
         DockerHub("ritclizup", "rit-python3-pyinstaller-builder"),
         DockerHub("ritclizup", "dennis-middleware"),
         DockerHub("ritclizup", "dennis-portal"),
         DockerHub("ritclizup", "rit-csharp-builder"),
         DockerHub("ritclizup", "rit-python2-runner"),
         DockerHub("ritclizup", "rit-python2-builder"),
         DockerHub("ritclizup", "rit-python3-runner"),
         DockerHub("ritclizup", "rit-python3-builder"),
         DockerHub("ritclizup", "rit-go-1.16-runner"),
         DockerHub("ritclizup", "rit-go-1.16-builder"),
         DockerHub("ritclizup", "rit-powershell-runner"),
         DockerHub("ritclizup", "rit-powershell-builder"),
         DockerHub("ritclizup", "rit-ruby-runner"),
         DockerHub("ritclizup", "rit-ruby-builder"),
         DockerHub("ritclizup", "rit-csharp-runner"),
         DockerHub("ritclizup", "rit-node-runner"),
         DockerHub("ritclizup", "rit-node-builder"),
         DockerHub("ritclizup", "rit-rust-builder"),
         DockerHub("ritclizup", "rit-rust-runner"),
         DockerHub("ritclizup", "rit-go-builder"),
         DockerHub("ritclizup", "rit-go-runner"),
         DockerHub("ritclizup", "rit-kotlin-jdk11-runner"),
         DockerHub("ritclizup", "rit-kotlin-jdk11-builder"),
         DockerHub("ritclizup", "rit-kotlin-jdk8-runner"),
         DockerHub("ritclizup", "rit-kotlin-jdk8-builder"),
         DockerHub("ritclizup", "rit-java11-builder"),
         DockerHub("ritclizup", "rit-java11-runner"),
         DockerHub("ritclizup", "rit-java8-builder"),
         DockerHub("ritclizup", "rit-java8-runner"),
         DockerHub("ritclizup", "rit-swift-builder"),
         DockerHub("ritclizup", "rit-swift-runner"),
         DockerHub("ritclizup", "rit-typescript-builder"),
         DockerHub("ritclizup", "rit-typescript-runner"),
         DockerHub("ritclizup", "rit-php-builder"),
         DockerHub("ritclizup", "rit-php-runner"),
         DockerHub("ritclizup", "rit-perl-builder"),
         DockerHub("ritclizup", "rit-perl-runner"),
         DockerHub("ritclizup", "rit-shell-bat-builder"),
         DockerHub("ritclizup", "rit-shell-bat-runner"),
         DockerHub("ritclizup", "pythonwithgo"),
         DockerHub("ritclizup", "rit_beagle_generate_scaffold-android"),
         DockerHub("ritclizup", "rit_scaffold_generate_coffee-go"),
         DockerHub("ritclizup", "rit_aws_list_bucket")
         }

"""Limpa dados antigos da planilha"""


def limpa_dados_antigos():
    logging.info("Limpando dados antigos")
    worksheet.clear(start='A1', end='F100')
    logging.info("Limpeza concluída")


"""Criar os cabeçalhos da planilha"""


def criar_headers():
    headers = ["name", "namespace", "description", "status", "stars", "pulls"]
    worksheet.append_table(headers, start='A1')
    logging.info("Cabeçalhos criados")


"""Faz a guarda dos dados extraídos em uma planilha definida no client_secret.json"""


def guardar_dados():
    logging.info("Tratando informacoes")
    name = image['data']['name']
    namespace = image['data']['namespace']
    status = image['data']['status']
    description = image['data']['full_description']
    stars = image['data']['star_count']
    pulls = image['data']['pull_count']
    new_row = [name, namespace, description, status, stars, pulls]
    worksheet.append_table(new_row, start='A2')
    logging.info("Inclusão na planilha feita com sucesso")


"""Ponto de início da rotina"""


def start():
    global image
    try:
        limpa_dados_antigos()
        criar_headers()
        for repo in repos:
            for image in repo.fetch():
                guardar_dados()
        logging.info("Extracao concluida com sucesso")
    except RuntimeError:
        raise Exception("Erro ao buscar os dados solicitados")


start()
