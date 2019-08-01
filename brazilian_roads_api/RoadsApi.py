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

    def _carregar_links_infracoes(self):
        """Função que busca o link para cada infração"""
        response = requests.get(self.url)

        # Recupera o HTML
        html_data = response.text
        # Cria um objeto BeautifulSoup a partir do HTML
        soup = BeautifulSoup(html_data, features="html.parser")

        links = soup.findAll("a", {"class": "internal-link"})

        # Filtra links referentes aos anos
        self.links_infracoes = {link.text: link['href'] for link in links
                                if link.text.startswith('20')}
