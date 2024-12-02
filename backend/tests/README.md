# Tests

Die Tests wurden in pytest implementiert.

## Erstellen von Tests

- Pytest erkennt die Tests am besten, wenn die Datei *tests_dateiname* benannt ist.
- Test-Funktionen erstellen, auf Import-Pfade für zu testende Module achten.

## Test-Ausführung

- Navigieren in Projektordner `HandScanAI/backend`.
- `python manage.py test`
- ODER `python -m pytest`: Eingabe zur Ausführung der Tests in Konsole (führt alle vorhandenen Tests aus und erstellt Testbericht).
- Hinzufügen von `-v` für verbose Log-Ausgabe
- Für weitere Anpassungen des pytest-commands, siehe [How to invoke pytest](https://docs.pytest.org/en/stable/how-to/usage.html).

## Anpassungen

Wenn für eine Pipeline etc. die Ausführung der Tests von `HandScanAI` statt `HandScanAI/backend` durchgeführt werden soll, reicht es, in den drei embeddings-Test-files bei den imports das "backend." hinzuzufügen.

Wird das gemacht, funktioniert die Testausführung nur noch von `HandScanAI` aus.
