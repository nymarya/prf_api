=======
PRF API
=======


.. image:: https://img.shields.io/pypi/v/prf-api.svg
        :target: https://pypi.python.org/pypi/prf-api

.. image:: https://img.shields.io/travis/nymarya/prf_api.svg
        :target: https://travis-ci.org/nymarya/prf_api

.. image:: https://img.shields.io/badge/license-MIT-red.svg
     :target: https://pyup.io/repos/github/nymarya/prf_api/
     :alt: Updates



API de dados abertos da PRF


Esta pacote tem o objetivo de facilitar o download e o uso dos `dados abertos da PRF`_, 
que contém informações sobre acidentes e infrações cometidas nas rodovias federais do Brasil.

Dependências
------------

Para baixar dados anteriores a 2018, é necessário instalar `unrar`.

**Para MacOS**

.. parsed-literal::

        brew install unrar


**Para Linux**

.. code::

        apt-get install unrar


Uso
----

O pacote pode ser obtido via `pip`.

.. code:: shell

        pip install prf-api


Para utlizar, basta instanciar a classe:

.. code:: python

  from prf_api import prf_api

  data = prf_api.PRFApi()

  data.baixar('infracoes', anos=list(range(2017, 2019)))

  df = data.dataframe('infracoes', anos=list(range(2017, 2019)), estado='RN')

Créditos
--------

Este pacote foi criado com Cookiecutter_ e o template `audreyr/cookiecutter-pypackage`_ .

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`dados abertos da PRF`: https://portal.prf.gov.br/portal/dados-abertos
