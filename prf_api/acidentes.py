from bs4 import BeautifulSoup


class Acidente:
    """ Classe responsável por manter atributos referentes a acidentes.

    Atributos
    ---------
    url: str
        url acessada para obter informações sobre acidentes
    links: list
        lista de códigos que formam o link para download.
    """

    def __init__(self):
        self.url = 'https://portal.prf.gov.br/dados-abertos-acidentes'
        self._tipo = ''
        self.links = {}

    def carregar_links(self, response, tipo):
        """ Carrega links disponíveis na página de infrações. """
        # Recupera o HTML
        html_data = response.text
        # Cria um objeto BeautifulSoup a partir do HTML
        soup = BeautifulSoup(html_data, features="html.parser")

        # Recupera título
        titulos = soup.findAll("h2")

        links = []

        # Busca links
        for i, tag in enumerate(titulos):
            titulo = tag.text
            # Checa título de H2, procura lista de links próximo
            if titulo == tipo:
                links = tag.find_next_sibling('ul').findAll('a')
                break

        # Filtra links referentes aos anos
        self.links[tipo] = {int(link.text.split('-')[0]): link['href'].split('/')[-1]
                            for link in links if link.text.startswith('20')}
