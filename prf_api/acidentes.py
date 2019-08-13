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
        self.url = 'https://www.prf.gov.br/portal/dados-abertos/acidentes/acidentes'
        self._tipo = ''

    def carregar_links(self, response):
        """ Carrega links disponíveis na página de infrações. """
        # Recupera o HTML
        html_data = response.text
        # Cria um objeto BeautifulSoup a partir do HTML
        soup = BeautifulSoup(html_data, features="html.parser")

        tables = soup.findAll("table", {"class": "listing"})

        for table in tables:
            title = table.find('tbody').find('tr').find('th').find('h2')
            if title == tipo:
                break

        # Filtra links referentes aos anos
        self.links = {int(link.text): link['href'].split('/')[-1]
                      for link in links if link.text.startswith('20')}


class AcidenteOcorrencia(Acidente):
    """ Classe responsável por manter atributos referentes a acidentes
    agrupados por ocorrência.
    """

    def __init__(self):
        self._tipo = 'Agrupados por ocorrência'


class AcidentePessoa(Acidente):
    """ Classe responsável por manter atributos referentes a acidentes
    agrupados por pessoa.
    """

    def __init__(self):
        self._tipo = 'Agrupados por pessoa'


class AcidenteAgrupado(Acidente):
    """ Classe responsável por manter atributos referentes a acidentes
    agrupados.
    """

    def __init__(self):
        self._tipo = 'Agrupados por pessoa - \
                Todas as causas e tipos de acidentes (a partir de 2017)'
