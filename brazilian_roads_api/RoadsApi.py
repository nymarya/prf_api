import requests
from bs4 import BeautifulSoup


class RoadsApi:
    """ Classe usada para manipular dados abertos da Polícia
    Rodoviária Federal.
    """

    def __init__(self):
        self.url = 'https://www.prf.gov.br/portal/dados-abertos/infracoes'
        self.download_url = 'https://www.prf.gov.br/arquivos/index.php/s/{}/download'

        self._carregar_links_infracoes()

    def _exibir_erro(self, ex: Exception, msg: str):
        """Exibir mensagem personalizada para erro

        Parâmetros
        ----------
        ex: Exception
            exceção que foi detectada
        msg: str
            mensagem personalizada para erro
        """
        print('\033[91m{}\033[0m'.format(msg))
        print(ex)

    def _carregar_links_infracoes(self):
        """Função que busca o link para cada infração"""
        try:
            response = requests.get(self.url)
        except requests.exceptions.ConnectionError as ex:
            self._exibir_erro(ex, "Falha de conexão. "
                              "Verifique sua conexão e tente novamente.")
            return
        except Exception as ex:
            self._exibir_erro(ex, "Ocorreu um erro inesperado. "
                              "Verifique sua conexão e tente novamente.")
            return

        # Recupera o HTML
        html_data = response.text
        # Cria um objeto BeautifulSoup a partir do HTML
        soup = BeautifulSoup(html_data, features="html.parser")

        links = soup.findAll("a", {"class": "internal-link"})

        # Filtra links referentes aos anos
        self.links_infracoes = {link.text: link['href'].split('/')[-1]
                                for link in links if link.text.startswith('20')}
