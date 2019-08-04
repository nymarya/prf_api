# brazilian-roads-api

Esta pacote tem o objetivo de facilitar o download e o uso dos [dados abertos da PRF](http://prf.gov.br/portal/dados-abertos), que contém informações sobre acidentes e infrações cometidas nas rodovias federais do Brasil.

## Dependências

Para baixar dados anteriores a 2018, é necessário instalar `unrar`.

**Para MacOS**

```
brew install unrar
```

**Para Linux**
```
apt-get install unrar
```

## Uso
O pacote pode ser obtido via `pip`.

```
pip install brazilian_roads_api
```

Para utlizar, basta instanciar a classe:

```python
from brazilian_roads_api import RoadsApi

data = RoadsApi()

data.baixar('infracoes', anos=list(range(2017, 2019)))

```
