from io import BytesIO
from zipfile import ZipFile
from rarfile import RarFile
import os


def extrair_rar(rf: RarFile, caminho: str):
    """ Extrai csvs de um arquivo . rar.

    Parâmetros
    ----------
    rf: Rarfile
        conteúdo do arquivo compactado.
    caminho: str
        caminho para pasta onde os arquivos devem ser salvos.
    """
    ano = caminho.split('/')[-1]
    n_arquivos = len(rf.infolist())
    for f in rf.infolist():
        # Filtra arquivos csvs comprimidos
        if f.filename.endswith('csv'):
            filename = f.filename.split('/')[-1]
            print("\033[94m>> Baixando {}/{}\033[0m".format(ano, filename))
            with open(caminho + '/' + filename, "wb") as of:
                of.write(rf.read(f.filename))


def extrair_zip(zp: ZipFile, caminho: str):
    """ Extrai csvs de um arquivo .zip.

    Parâmetros
    ----------
    zp: ZipFile
        conteúdo do arquivo compactado.
    caminho: str
        caminho para pasta onde os arquivos devem ser salvos.
    """
    ano = caminho.split('/')[-1]
    for f in zp.namelist():
        if f.endswith('csv'):
            filename = f.split('/')[-1]
            print("\033[94m>> Baixando {}/{}\033[0m".format(ano, filename))
            with open(caminho + '/' + filename, "wb") as of:
                of.write(zp.read(f))


def extrair_arquivos(tipo: str, caminho: str, conteudo):
    """ Extrai csvs de um arquivo compactado.

    Parâmetros
    ----------
    tipo: str
        tipo do arquivo: rar ou zip.
    caminho: str
        caminho para pasta onde os arquivos devem ser salvos.
    conteudo
        bytes do arquivo compactado.
    """
    if tipo == "x-rar-compressed":
        # Salva temporariamente o .rar
        with open('file.rar', 'wb') as f:
            f.write(conteudo)
        # Extrai arquivos csv
        with RarFile("file.rar") as rf:
            extrair_rar(rf, caminho)

        # Apaga .rar
        os.remove('file.rar')
    else:
        zipfile = ZipFile(BytesIO(conteudo))
        with zipfile as zp:
            extrair_zip(zp, caminho)
