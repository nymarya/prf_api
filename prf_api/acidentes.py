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

    def carregar_links(self, response, tipo: str):
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

class AcidenteOcorrencia:
    """ Classe responsável por manter atributos referentes a acidentes
    agrupados por ocorrência.
    """
