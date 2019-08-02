import requests
import os
from .Infracoes import Infracoes
from .arquivo import extrair_arquivos


class RoadsApi:
    """ Classe usada para manipular dados abertos da Polícia
    Rodoviária Federal.
    """

    def __init__(self):
        self.url = 'https://www.prf.gov.br/portal/dados-abertos/infracoes'
        self.download_url = 'https://www.prf.gov.br/arquivos/index.php/s/{}/download'

        self._carregar_links()

    def _exibir_erro(self, msg: str, ex: Exception = None):
        """Exibir mensagem personalizada para erro

        Parâmetros
        ----------
        ex: Exception
            exceção que foi detectada
        msg: str
            mensagem personalizada para erro
        """
        print('\033[91m{}\033[0m'.format(msg))
        if ex is not None:
            print(ex)
        print()

    def _carregar_links(self):
        """Função que busca o link para cada infração"""
        self.infracoes = Infracoes()
        try:
            response_infracoes = requests.get(self.infracoes.url)
        except requests.exceptions.ConnectionError as ex:
            self._exibir_erro("Falha de conexão. "
                              "Verifique sua conexão e tente novamente.", ex)
            return
        except Exception as ex:
            self._exibir_erro("Ocorreu um erro inesperado. "
                              "Verifique sua conexão e tente novamente.", ex)
            return

        self.infracoes.carregar_links(response_infracoes)

    def _criar_diretorio(self, caminho: str) -> str:
        """Cria o diretório, caso ele não exista.
        Parâmetros
        ----------
        path: str
            o caminho da pasta onde serão adicionados os arquivos."""
        if not os.path.exists(caminho):
            os.makedirs(caminho)

        return caminho

    def baixar(self, tipo: {'infracoes', 'acidentes'},
               anos: list, caminho: str = os.getcwd()):
        """Realiza o download dos conjuntos de dados de acordo com o
        tipo desejado

        Parâmetros
        ----------
        tipo : {'infracoes', 'acidentes'}
            tipo de dados que se deseja realizar o download (por padrão,
            'infracoes')
        caminho: str
            o caminho da pasta onde serão adicionados os arquivos
            (por padrão, a pasta atual).
        anos: list
            lista de anos dos dados
        """
        dados = self.infracoes if tipo == 'infracoes' else ''

        # Checa se os anos são válidos
        for ano in anos:
            if not (ano in dados.links.keys()):
                self._exibir_erro("Ano {} não disponível".format(ano))
                return

        # Realiza o download
        caminho = self._criar_diretorio('{}/{}'.format(caminho, tipo))
        for ano in anos:
            try:
                link = self.download_url.format(dados.links[ano])
                print("Buscando datasets de {} para o ano {}...".format(tipo, ano))
                dataset = requests.get(link)
            except requests.exceptions.ConnectionError as ex:
                self._exibir_erro("Falha de conexão. "
                                  "Verifique sua conexão e tente novamente.", ex)
            except Exception as ex:
                self._exibir_erro("Ocorreu um erro inesperado. "
                                  "Verifique sua conexão e tente novamente.", ex)
            diretorio = self._criar_diretorio('{}/{}'.format(caminho, ano))

            # Carrega e descompacta arquivo comprimido
            formato_arquivo = dataset.headers['Content-Type'].split('/')[-1]
            extrair_arquivos(formato_arquivo, diretorio, dataset.content)
