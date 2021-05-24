from bs4 import BeautifulSoup


class Infracoes:
    """ Classe responsável por manter atributos referentes a infrações.

    Atributos
    ---------
    url: str
        url acessada para obter informações sobre infrações
    links: list
        lista de códigos que formam o link para download.
    """

    def __init__(self):
        self.url = 'https://portal.prf.gov.br/dados-abertos-infracoes'

    def carregar_links(self, response):
        """ Carrega links disponíveis na página de infrações. """
        # Recupera o HTML
        html_data = response.text
        # Cria um objeto BeautifulSoup a partir do HTML
        soup = BeautifulSoup(html_data, features="html.parser")

        links = soup.findAll("a")
        # Filtra links referentes aos anos
        self.links = {int(link.text): link['href'].split('/')[-1]
                      for link in links if link.text.startswith('20')}
