# -*- coding: utf-8 -*-

import requests
import os
from .infracoes import Infracoes
from .acidentes import Acidente
from .arquivo import extrair_arquivos
import pandas as pd


class PRFApi:
    """ Classe principal usada para manipular dados abertos da Polícia
    Rodoviária Federal.
    """

    TIPOS = {'infracoes': 'infracoes',
             'acidentes_pessoa': 'Agrupados por pessoa',
             'acidentes_ocorrencia': 'Agrupados por ocorrência',
             'acidentes_agrupados': 'Agrupados por pessoa - \
Todas as causas e tipos de acidentes (a partir de 2017)'}

    # Mapeamento de coluna que deve ser
    # filtrada para cada localidade e cada
    # tipo de conjunto
    COLUNAS = {
        'infracoes': {
            'estado': 'uf_infracao'
        },
        'acidentes_pessoa': {'estado': 'uf'},
        'acidentes_ocorrencia': {'estado': 'uf'},
        'acidentes_agrupados': {'estado': 'uf'},
    }

    REGIOES = {
        'CO': ['DF', 'GO', 'MS', 'MT'],
        'N': ['AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO'],
        'NE': ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'],
        'S': ['PR', 'RS', 'SC'],
        'SE': ['ES', 'MG', 'RJ', 'SP']
    }

    def __init__(self):
        self.url = 'https://www.prf.gov.br/portal/dados-abertos-infracoes'
        self.download_url = 'http://arquivos.prf.gov.br/arquivos/index.php/s/{}/download'

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
        self.acidentes = Acidente()
        try:
            response_infracoes = requests.get(self.infracoes.url)
            response_acidentes = requests.get(self.acidentes.url)
        except requests.exceptions.ConnectionError as ex:
            self._exibir_erro("Falha de conexão. "
                              "Verifique sua conexão e tente novamente.", ex)
            return
        except Exception as ex:
            self._exibir_erro("Ocorreu um erro inesperado. "
                              "Verifique sua conexão e tente novamente.", ex)
            return

        self.infracoes.carregar_links(response_infracoes)
        for tipo in self.TIPOS.values():
            if tipo is not "infracoes":
                self.acidentes.carregar_links(response_acidentes, tipo)

    def _criar_diretorio(self, caminho: str) -> str:
        """Cria o diretório, caso ele não exista.
        Parâmetros
        ----------
        path: str
            o caminho da pasta onde serão adicionados os arquivos."""
        if not os.path.exists(caminho):
            os.makedirs(caminho)

        return caminho

    def _filtrar_dataframe(self, df: pd.DataFrame, coluna: str,
                           area: {str, list}) -> pd.DataFrame:
        """ Filtra dataframe de acordo com estado ou área.

        Parâmetros
        ----------
        df: pd.DataFrame
            dataframe sobre o qual se aplica a filtragem
        coluna: str
            coluna sobre a qual se aplica o filtro
        area: str  ou list
            estado (sigla) ou regiao (lista de estados)
        """
        if type(area) == str:
            query = " {} == '{}'"
        elif type(area) == list:
            query = "{} in {}"
        else:
            self._exibir_erro("Área {} não disponível".format(area))

        return df.query(query.format(coluna, area))

    def baixar(self, tipo: {'infracoes', 'acidentes_pessoa',
               'acidentes_ocorrencia', 'acidentes_agrupados'},
               anos: list = None, caminho: str = os.getcwd()):
        """Realiza o download dos conjuntos de dados de acordo com o
        tipo desejado

        Parâmetros
        ----------
        tipo : {'infracoes', 'acidentes_pessoa', 'acidentes_ocorrencia',
                'acidentes_agrupados'}
            tipo de dados que se deseja realizar o download (por padrão,
            'infracoes')
        caminho: str
            o caminho da pasta onde serão adicionados os arquivos
            (por padrão, a pasta atual).
        anos: list
            lista de anos dos dados
        """
        if tipo not in self.TIPOS.keys():
            self._exibir_erro("Tipo '{}' é inválido. ".format(tipo))
            return

        if tipo == "infracoes":
            links = self.infracoes.links
        else:
            links = self.acidentes.links[self.TIPOS[tipo]]

        # Se não for passada uma lista, baixar todo os anos
        if anos is None:
            anos = links.keys()

        # Checa se os anos são válidos
        for ano in anos:
            if not (ano in links.keys()):
                self._exibir_erro("Ano {} não disponível".format(ano))

        # Realiza o download
        caminho = self._criar_diretorio('{}/{}'.format(caminho, tipo))
        for ano in anos:
            try:
                link = self.download_url.format(links[ano])
                print("Buscando datasets de {} para o ano {}...".format(tipo,
                                                                        ano))
                dataset = requests.get(link)
                diretorio = self._criar_diretorio('{}/{}'.format(caminho, ano))

                # Carrega e descompacta arquivo comprimido
                formato_arquivo = dataset.headers['Content-Type'].split('/')[-1]
                extrair_arquivos(formato_arquivo, diretorio, dataset.content)
            except requests.exceptions.ConnectionError as ex:
                self._exibir_erro("Falha de conexão. "
                                  "Verifique sua conexão e tente novamente.", ex)
            except Exception as ex:
                self._exibir_erro("Ocorreu um erro inesperado. "
                                  "Verifique sua conexão e tente novamente.", ex)            

    def dataframe(self, tipo: {'infracoes', 'acidentes_pessoa',
                  'acidentes_ocorrencia', 'acidentes_agrupados'},
                  anos: list = None, caminho: str = os.getcwd(),
                  estado: str = None,
                  regiao: {'CO', 'N', 'NE', 'S', 'SE'}=None) -> pd.DataFrame:
        """Trasforma os csvs em dataframes.

        Parâmetros
        ----------
        tipo : {'infracoes', 'acidentes_pessoa', 'acidentes_ocorrencia',
                'acidentes_agrupados'}
            tipo de dados que se deseja realizar o download (por padrão,
            'infracoes')
        caminho: str
            o caminho da pasta onde serão adicionados os arquivos
            (por padrão, a pasta atual).
        anos: list
            lista de anos dos dados.
        estado: str
            sigla do estado que servirá para a filtragem.
        regiao: {'CO','N', 'NE', 'S', 'SE'}
            sigla da região cujos estados serão filtrados.

        Retorno
        -------
        dataframe com todos os dados.
        """
        # Verifica se tipo é válido
        if tipo not in self.TIPOS.keys():
            self._exibir_erro("Tipo '{}' é inválido. ".format(tipo))
            return

        if tipo == "infracoes":
            links = self.infracoes.links
        else:
            links = self.acidentes.links[self.TIPOS[tipo]]

        # Se não for passada uma lista, baixar todo os anos
        if anos is None:
            anos = links.keys()

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
                try:
                    df = pd.read_csv(caminho_arquivo, encoding='latin1')
                except pd.errors.ParserError:
                    # Checa se o csv foi separado corretamente
                    df = pd.read_csv(caminho_arquivo, encoding='latin1',
                                     sep=';')

                # Checa se o csv foi separado corretamente
                if len(df.columns) == 1:
                    df = pd.read_csv(caminho_arquivo, encoding='latin1',
                                     sep=';')

                coluna = self.COLUNAS[tipo]['estado']
                # Realiza a filtragem, se algum parâmetro de busca for usado
                if estado is not None:
                    df = self._filtrar_dataframe(df, coluna, estado)
                elif regiao is not None:
                    # Filtra todos os estados da região
                    df = self._filtrar_dataframe(df, coluna,
                                                 self.REGIOES[regiao])
                dataframe = dataframe.append(df, ignore_index=True)

                del df  # Libera memória

        return dataframe
