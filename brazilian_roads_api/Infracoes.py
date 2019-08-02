from bs4 import BeautifulSoup

class Infracoes:

    def __init__(self):
        self.url = 'https://www.prf.gov.br/portal/dados-abertos/infracoes'

    def carregar_links(self, response):
        # Recupera o HTML
        html_data = response.text
        # Cria um objeto BeautifulSoup a partir do HTML
        soup = BeautifulSoup(html_data, features="html.parser")

        links = soup.findAll("a", {"class": "internal-link"})

        # Filtra links referentes aos anos
        self.links = {int(link.text): link['href'].split('/')[-1]
                      for link in links if link.text.startswith('20')}
