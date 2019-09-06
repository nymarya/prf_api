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
        self.url = 'https://portal.prf.gov.br/portal/dados-abertos/acidentes/acidentes'
        self._tipo = ''
        self.links = {}

    def carregar_links(self, response, tipo):
        """ Carrega links disponíveis na página de infrações. """
        # Recupera o HTML
        html_data = response.text
        # Cria um objeto BeautifulSoup a partir do HTML
        soup = BeautifulSoup(html_data, features="html.parser")

        # Recupera tabelas com título
        tabelas = soup.findAll("table", {"class": "listing"})

        # Recupera tabelas com links
        tabelas_links = soup.findAll("table", {"class": "plain"})

        links = []

        # Busca links
        for i, tabela in enumerate(tabelas):
            titulo = tabela.find('tbody').find('tr').find('th').find('h2')
            # Checa título da tabela
            if titulo.text == tipo:
                links = tabelas_links[i].findAll('a')
                break

        # Filtra links referentes aos anos
        self.links[tipo] = {int(link.text.split('-')[0]): link['href'].split('/')[-1]
                            for link in links if link.text.startswith('20')}
