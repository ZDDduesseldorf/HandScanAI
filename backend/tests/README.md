# Tests

Die Tests wurden in pytest implementiert.

## Erstellen von Tests

- Pytest erkennt die Tests am besten, wenn die Datei *tests_dateiname* benannt ist.
- Test-Funktionen erstellen, auf Import-Pfade für zu testende Module achten.

## Test-Ausführung

- Mithilfe des Plugins: Tests auswählen und ausführen
- In Konsole: Sicherstellen, dass man sich im Ordner `HandScanAI/backend` befindet.
- Ausführen von `python manage.py test`
- ODER `python -m pytest`. An diesen Command kann man noch zusätzliche commandline-flags anhängen. Beispiele:
  - Hinzufügen von `-v` für verbose Ausgabe
  - Hinzufügen von `-s`, damit print-Befehle während dem Test ebenfalls auf der Konsole ausgegeben werden
  - Für weitere Anpassungen des pytest-commands, siehe [How to invoke pytest](https://docs.pytest.org/en/stable/how-to/usage.html).

## Anpassungen

Wenn für eine Pipeline etc. die Ausführung der Tests von `HandScanAI` statt `HandScanAI/backend` aus durchgeführt werden soll, müssen die Importe der betroffenen Module um ein `backend.` erweitert werden, damit die PFade wieder gültig sind.

Wird das gemacht, funktioniert die Testausführung nur noch von `HandScanAI` aus.
