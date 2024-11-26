# Tests

Die Tests wurden in pytest implementiert.

Diese Readme betrifft die implementierten Backend-Tests. Für Frontend-Tests, bitte die Readme ergänzen.

## Environment

Aktivieren und Einrichten der virtuellen Umgebung (siehe README backend). Zusätzliche Installation von pytest durch die `requirements.txt`:

```sh
pip install -r requirements.txt
```

(nach Zusammenführung des Dependency-Managements kann dieser Teil gelöscht werden)

## Erstellen von Tests

- Pytest erkennt die Tests am besten, wenn die Datei *tests_dateiname* benannt ist.
- Test-Funktionen erstellen, auf Import-Pfade für zu testende Module achten.

## Test-Ausführung

- Navigieren in Projektordner `HandScanAI` (**nicht** in Unterordner `tests`, da dieser automatisch von pytest erkannt wird).
- `python -m pytest`: Eingabe zur Ausführung der Tests in Konsole (führt alle vorhandenen Tests aus und erstellt Testbericht).
- Für Ausführung bestimmter Tests, siehe [How to invoke pytest](https://docs.pytest.org/en/stable/how-to/usage.html).
