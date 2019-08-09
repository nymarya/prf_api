#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prf_api` package."""

import pytest

from click.testing import CliRunner

from prf_api import prf_api
from prf_api import cli
import os


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_init():
    """Sample pytest test function with the pytest fixture as an argument."""
    prf_data = prf_api.PRFApi()
    prf_data.baixar('infracoes', anos=[2018, 2019])
    caminho = os.getcwd() + "/infracoes"
    assert os.path.exists(caminho)
    assert os.path.exists(caminho + "/2018")
    for mes in ['abr', 'ago', 'dez', 'fev', 'jan', 'jul',
                'jun', 'mai', 'mar', 'nov', 'out', 'set']:
        assert os.path.exists(caminho + "/2018/" + mes + ".csv")


def test_dataframe():
    """ Testa criação de dataframe"""
    prf_data = prf_api.PRFApi()
    df = prf_data.dataframe('infracoes', anos=list(range(2017, 2019)),
                            estado='RN')
    assert df.uf_infracao.unique() == ['RN']

    anos = df.dat_infracao.str.split('-', n=1, expand=True)[0].unique()
    assert sorted(anos) == ['2017', '2018']
    assert len(df.columns) == 22


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'prf_api.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
