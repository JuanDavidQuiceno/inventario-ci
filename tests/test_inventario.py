import pytest

from inventario import __version__
from inventario.core import Inventario, InventarioError
from inventario.servidor import estado


@pytest.fixture
def inv():
    inventario = Inventario()
    inventario.agregar("teclado", 10, 45000)
    return inventario


def test_agregar_producto_nuevo(inv):
    assert inv.cantidad("teclado") == 10


def test_agregar_suma_a_existente(inv):
    inv.agregar("teclado", 5)
    assert inv.cantidad("teclado") == 15


def test_retirar_descuenta(inv):
    inv.retirar("teclado", 3)
    assert inv.cantidad("teclado") == 7


def test_retirar_mas_de_lo_disponible_falla(inv):
    with pytest.raises(InventarioError):
        inv.retirar("teclado", 50)


def test_retirar_producto_inexistente_falla(inv):
    with pytest.raises(InventarioError):
        inv.retirar("monitor", 1)


def test_valor_total(inv):
    inv.agregar("mouse", 2, 20000)
    assert inv.valor_total() == 10 * 45000 + 2 * 20000


def test_estado_del_servicio():
    assert estado() == {"estado": "ok", "version": __version__}
