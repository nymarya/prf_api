from io import BytesIO
from zipfile import ZipFile
from rarfile import RarFile
import os


def extrair_arquivos(tipo: str, caminho, conteudo):

    if tipo == "x-rar-compressed":
        # Salva temporariamente o .rar
        with open('file.rar', 'wb') as f:
            f.write(conteudo)
        # Extrai arquivos csv
        with RarFile("file.rar") as rf:
            for f in rf.infolist():
                # Filtra arquivos csvs comprimidos
                if f.filename.endswith('csv'):
                    filename = f.filename.split('/')[-1]
                    print("\033[91m>> Baixando {}\033[0m".format(f.filename))
                    with open(caminho + '/' + filename, "wb") as of:
                        of.write(rf.read(f.filename))

        # Apaga .rar
        os.remove('file.rar')
    else:
        zipfile = ZipFile(BytesIO(conteudo))
        with zipfile as zp:
            for f in zp.namelist():
                if f.endswith('csv'):
                    filename = f.split('/')[-1]
                    print("\033[91m>> Baixando {}\033[0m".format(f))
                    with open(caminho + '/' + filename, "wb") as of:
                        of.write(zp.read(f))
