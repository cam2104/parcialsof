# test_caminos.py - Parte 4: casos de caja blanca (un caso por camino independiente)
# Base: p=3 (tramo 1), urbana, cliente normal, dia 1, sin cupon, sin flag.
# Los resultados esperados salen de la ESPECIFICACION, no del codigo heredado.
import pytest
from envios import calc

# (id, camino, entradas, esperado)  -- esperado = numero, o ValueError
CAMINOS = [
    ("CB-01", "P1 base", (3, "urbana", "normal", 1, None), 6000),
    ("CB-02", "P2 p<=0", (0, "urbana", "normal", 1, None), ValueError),
    ("CB-03", "P3 p>PMAX", (51, "urbana", "normal", 1, None), ValueError),
    ("CB-04", "P4 tramo 2", (5, "urbana", "normal", 1, None), 9000),
    ("CB-05", "P5 tramo 3", (12, "urbana", "normal", 1, None), 10600),
    ("CB-06", "P6 rural", (3, "rural", "normal", 1, None), 7500),
    ("CB-07", "P7 nacional", (3, "nacional", "normal", 1, None), 8700),
    ("CB-08", "P8 zona invalida", (3, "insular", "normal", 1, None), ValueError),
    ("CB-09", "P9 sabado", (3, "urbana", "normal", 6, None), 8000),
    ("CB-10", "P10 frecuente", (3, "urbana", "frecuente", 1, None), 5700),
    ("CB-11", "P11 vip", (3, "urbana", "vip", 1, None), 5100),
    ("CB-12", "P12 cupon ENVIO10", (3, "urbana", "normal", 1, "ENVIO10"), 5400),
    ("CB-13", "P13 cupon invalido", (3, "urbana", "normal", 1, "DESC50"), ValueError),
    ("CB-14", "P14 minimo 5000", (3, "urbana", "vip", 1, "ENVIO10"), 5000),
]


@pytest.mark.parametrize(
    "id_caso,camino,entradas,esperado",
    CAMINOS,
    ids=[c[0] for c in CAMINOS],
)
def test_camino_independiente(id_caso, camino, entradas, esperado):
    if esperado is ValueError:
        with pytest.raises(ValueError):
            calc(*entradas)
    else:
        assert calc(*entradas) == esperado


def test_cb15_camino_flag(capsys):
    """CB-15 / P15: flag=True imprime el costo (camino que usa el argumento flag)."""
    assert calc(3, "urbana", "normal", 1, None, True) == 6000
    assert "costo:" in capsys.readouterr().out