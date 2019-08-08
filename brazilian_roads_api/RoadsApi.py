import requests
import os
from .Infracoes import Infracoes
from .arquivo import extrair_arquivos
import pandas as pd

class RoadsApi:
    """ Classe usada para manipular dados abertos da Polícia
    Rodoviária Federal.
    """

    TIPOS = ['infracoes', 'acidentes']

    # Mapeamento de coluna que deve ser 
    # filtrada para cada localidade e cada
    # tipo de conjunto
    COLUNAS = {
        'infracoes': {
            'estado': 'uf_infracao'
        }
    }

    REGIOES = {
        'CO': ['DF', 'GO', 'MS', 'MT'],
        'N': ['AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO'],
        'NE': ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'],
        'S': ['PR', 'RS', 'SC'],
        'SE': ['ES', 'MG', 'RJ', 'SP']
    }

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
        if tipo not in self.TIPOS:
            self._exibir_erro("Tipo '{}' é inválido. ".format(tipo))
            return

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

    def dataframe(self, tipo: {'infracoes', 'acidentes'},
                  anos: list, caminho: str = os.getcwd(), estado: str = None,
                  regiao: {'CO','N', 'NE', 'S', 'SE'} = None) -> pd.DataFrame:
        """Trasforma os csvs em dataframes.

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
        estado: str
            sigla do estado que servirá para a filtragem
        regiao: {'CO','N', 'NE', 'S', 'SE'}
            sigla da região cujos estados serão filtrados
        Retorno
        -------
        dataframe com todos os dados.
        """
        # Verifica se tipo é válido
        if tipo not in self.TIPOS:
            self._exibir_erro("Tipo '{}' é inválido. ".format(tipo))
            return
        
        # Verifica se estado é válido
        estados = [x for regiao in list(self.REGIOES.values()) for x in regiao]
        if (estado is not None) and (estado not in estados):
            self._exibir_erro("Estado '{}' é inválido. ".format(estado))
            return  

        # Verifica se região é válida
        if (regiao is not None) and (regiao not in self.REGIOES.keys()):
            self._exibir_erro("Região '{}' é inválida. ".format(regiao))
            return   
        
        # Verifica se todos os anos foram baixados
        for ano in anos:
            pasta = '{}/{}/{}'.format(caminho, tipo, ano)
            if not os.path.exists(pasta):
                # Se não estiver baixado, realizar o download
                self.baixar(tipo, [ano], caminho)

        # Recupera csvs e cria dataframe
        dataframe = pd.DataFrame()  # Cria df vazio
        for ano in anos:
            print(">>> Criando dataframe com ano {}...".format(ano))
            pasta = '{}/{}/{}'.format(caminho, tipo, ano)
            for arquivo in os.listdir(pasta):
                caminho_arquivo = '{}/{}'.format(pasta, arquivo)
                df = pd.read_csv(caminho_arquivo, encoding='latin1')
                # Realiza a filtragem, se algum parâmetro de busca for usado
                if estado is not None:
                    coluna = self.COLUNAS[tipo]['estado']
                    df = df.query( " {} == '{}'".format(coluna, estado))
                elif regiao is not None:
                    # Filtra todos os estados da região
                    regioes = self.REGIOES[regiao]
                    coluna = self.COLUNAS[tipo]['estado']
                    df = df.query( " {} in {}".format(coluna, regioes))  #TODO: tranformar em função privada
                dataframe = dataframe.append(df, ignore_index=True)

                del df  # Libera memória

        return dataframe
