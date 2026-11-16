import pytest

from cambio import calcular_resumos


def test_variacao_positiva():
    rates = {"BRL": 7.5}
    historico = {
        "2026-11-01": {"BRL": 6.0},
        "2026-11-02": {"BRL": 8.0},
    }

    resumos = calcular_resumos(rates, historico)

    assert resumos["BRL"]["hoje"] == 7.5
    assert resumos["BRL"]["media"] == pytest.approx(7.0)
    assert resumos["BRL"]["variacao"] == pytest.approx(7.142857, rel=1e-4)


def test_variacao_negativa():
    rates = {"USD": 1.2}
    historico = {
        "2026-11-01": {"USD": 1.4},
        "2026-11-02": {"USD": 1.2},
    }

    resumos = calcular_resumos(rates, historico)

    assert resumos["USD"]["hoje"] == 1.2
    assert resumos["USD"]["media"] == pytest.approx(1.3)
    assert resumos["USD"]["variacao"] == pytest.approx(-7.6923, rel=1e-4)


def test_variacao_zero():
    rates = {"USD": 1.3}
    historico = {
        "2026-11-01": {"USD": 1.2},
        "2026-11-02": {"USD": 1.4},
    }

    resumos = calcular_resumos(rates, historico)

    assert resumos["USD"]["variacao"] == pytest.approx(0.0, abs=1e-9)


def test_duas_moedas_independentes():
    rates = {"BRL": 7.5, "USD": 1.2}
    historico = {
        "2026-11-01": {"BRL": 6.0, "USD": 1.4},
        "2026-11-02": {"BRL": 8.0, "USD": 1.2},
    }

    resumos = calcular_resumos(rates, historico)

    assert resumos["BRL"]["media"] == pytest.approx(7.0)
    assert resumos["USD"]["media"] == pytest.approx(1.3)
    assert resumos["BRL"]["variacao"] > 0
    assert resumos["USD"]["variacao"] < 0


def test_historico_vazio_nao_quebra():
    resumos = calcular_resumos({"BRL": 7.5}, {})
    

    assert "BRL" not in resumos