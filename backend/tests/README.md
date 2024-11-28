# Tests

Die Tests wurden in pytest implementiert.

## Erstellen von Tests

- Pytest erkennt die Tests am besten, wenn die Datei *tests_dateiname* benannt ist.
- Test-Funktionen erstellen, auf Import-Pfade für zu testende Module achten.

## Test-Ausführung

- Navigieren in Projektordner `HandScanAI` (**nicht** in Unterordner `tests`, da dieser automatisch von pytest erkannt wird).
- `python -m pytest`: Eingabe zur Ausführung der Tests in Konsole (führt alle vorhandenen Tests aus und erstellt Testbericht).
- Für Ausführung bestimmter Tests, siehe [How to invoke pytest](https://docs.pytest.org/en/stable/how-to/usage.html).

## Ruff-Linter

Der Ruff-Linter hat Probleme mit den Assertions in den Tests. Das sollte für die Pipeline und lokal ignoriert werden (Bspw: [Stackoverflow](https://stackoverflow.com/questions/68428293/s101-use-of-assert-detected-for-python-tests)).
