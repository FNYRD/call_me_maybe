"""Conftest compartido de tests/. Hoy solo sirve al resumen agregado de
test_bloque_7.py (cuantos prompts acerto cada proyecto) — no toca nada de
test_bloque_6.py."""
import pytest


class _ResumenComparativo:
    def __init__(self) -> None:
        self.total = 0
        self.mio_correcto = 0
        self.companero_correcto = 0

    def registrar(self, mio_ok: bool, companero_ok: bool) -> None:
        self.total += 1
        self.mio_correcto += int(mio_ok)
        self.companero_correcto += int(companero_ok)


_RESUMEN_COMPARATIVO = _ResumenComparativo()


@pytest.fixture(scope="session")
def resumen_comparativo() -> _ResumenComparativo:
    return _RESUMEN_COMPARATIVO


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    if _RESUMEN_COMPARATIVO.total == 0:
        return
    terminalreporter.write_sep("=", "Resumen comparativo test_bloque_7")
    terminalreporter.write_line(f"Prompts evaluados: {_RESUMEN_COMPARATIVO.total}")
    terminalreporter.write_line(
        f"Mi proyecto acerto: {_RESUMEN_COMPARATIVO.mio_correcto}/{_RESUMEN_COMPARATIVO.total}"
    )
    terminalreporter.write_line(
        f"Proyecto del companero acerto: {_RESUMEN_COMPARATIVO.companero_correcto}/{_RESUMEN_COMPARATIVO.total}"
    )
