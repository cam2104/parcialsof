# test_envios.py - suite de caja negra (Parte 3) automatizada con pytest
# Parametros: A=4 B=1 C=0 D=0 E=7 F=7 -> PMAX=50, L1=3 (incluido), L2=10,
# RR=25%, RN=45%, V=15%, S=$2.000 (despues de descuentos), ambos descuentos,
# cupon inexistente = error.
import pytest
from envios import calc

# (id, requisito, (peso, zona, cliente, dia, cupon), esperado)
CASOS_VALOR = [
    ("TC-02", "R1,R3", (0.1, "urbana", "normal", 2, None), 6000),
    ("TC-03", "R3", (3, "urbana", "normal", 2, None), 6000),
    ("TC-04", "R3", (3.1, "urbana", "normal", 2, None), 9000),
    ("TC-05", "R3", (10, "urbana", "normal", 2, None), 9000),
    ("TC-06", "R3,R8", (10.1, "urbana", "normal", 2, None), 9100),
    ("TC-07", "R1,R3", (50, "urbana", "normal", 2, None), 41000),
    ("TC-10", "R4,R8", (5, "rural", "normal", 3, None), 11300),
    ("TC-11", "R4,R8", (5, "nacional", "normal", 3, None), 13100),
    ("TC-15", "R5", (5, "urbana", "normal", 6, None), 11000),
    ("TC-16", "R5", (5, "urbana", "normal", 7, None), 11000),
    ("TC-17", "R5", (5, "urbana", "normal", 5, None), 9000),
    ("TC-19", "R3-R6", (3.5, "rural", "vip", 6, "ENVIO10"), 10600),
    ("TC-20", "R3-R6", (12, "nacional", "frecuente", 7, None), 16600),
    ("TC-21", "R6,R8", (10, "urbana", "frecuente", 1, "ENVIO10"), 7700),
    ("TC-34", "R5,R6", (3, "urbana", "vip", 7, None), 7100),  # aisla DEF-02
    # Tabla de decision cliente x cupon x fin de semana (p=3, urbana)
    ("TD-01", "R6", (3, "urbana", "normal", 1, None), 6000),
    ("TD-02", "R5", (3, "urbana", "normal", 6, None), 8000),
    ("TD-03", "R6", (3, "urbana", "normal", 1, "ENVIO10"), 5400),
    ("TD-04", "R5,R6", (3, "urbana", "normal", 6, "ENVIO10"), 7400),
    ("TD-05", "R6", (3, "urbana", "frecuente", 1, None), 5700),
    ("TD-06", "R5,R6", (3, "urbana", "frecuente", 6, None), 7700),
    ("TD-07", "R6,R8", (3, "urbana", "frecuente", 1, "ENVIO10"), 5100),
    ("TD-08", "R5,R6,R8", (3, "urbana", "frecuente", 6, "ENVIO10"), 7100),
    ("TD-09", "R6,R8", (3, "urbana", "vip", 1, None), 5100),
    ("TD-10", "R5,R6,R8", (3, "urbana", "vip", 6, None), 7100),
    ("TD-11", "R6,R8", (3, "urbana", "vip", 1, "ENVIO10"), 5000),
    ("TD-12", "R5,R6,R8", (3, "urbana", "vip", 6, "ENVIO10"), 6600),
]

CASOS_ERROR = [
    ("TC-01", "R1", (0, "urbana", "normal", 2, None)),
    ("TC-08", "R1", (50.1, "urbana", "normal", 2, None)),
    ("TC-09", "R1", (-5, "urbana", "normal", 2, None)),
    ("TC-12", "R2", (5, "insular", "normal", 3, None)),
    ("TC-13", "R2", (5, "urbana", "normal", 0, None)),
    ("TC-14", "R2", (5, "urbana", "normal", 8, None)),
    ("TC-18", "R7", (5, "urbana", "normal", 3, "DESC50")),
]


@pytest.mark.parametrize(
    "id_caso,req,entradas,esperado",
    CASOS_VALOR,
    ids=[c[0] for c in CASOS_VALOR],
)
def test_resultado_esperado(id_caso, req, entradas, esperado):
    assert calc(*entradas) == esperado


@pytest.mark.parametrize(
    "id_caso,req,entradas",
    CASOS_ERROR,
    ids=[c[0] for c in CASOS_ERROR],
)
def test_entradas_invalidas_lanzan_error(id_caso, req, entradas):
    with pytest.raises(ValueError):
        calc(*entradas)


def test_mensaje_peso_invalido_exacto():
    """TC-01b (R1): el mensaje debe ser exactamente 'peso inválido'."""
    with pytest.raises(ValueError, match="peso inválido"):
        calc(0, "urbana", "normal", 2)