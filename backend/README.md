# HandScanAI Backend

## Inhaltsverzeichnis

- [HandScanAI Backend](#handscanai-backend)
  - [Inhaltsverzeichnis](#inhaltsverzeichnis)
  - [Installation](#installation)
    - [Python installieren](#python-installieren)
    - [Virtuelle Umgebung erstellen](#virtuelle-umgebung-erstellen)
    - [Virtuelle Umgebung aktivieren](#virtuelle-umgebung-aktivieren)
    - [Abhängigkeiten installieren](#abhängigkeiten-installieren)
    - [Server starten](#server-starten)
  - [Entwicklung in VSCode](#entwicklung-in-vscode)
    - [Extensions](#extensions)
    - [Python Interpreter einstellen](#python-interpreter-einstellen)
  - [Projektstruktur](#projektstruktur)
    - [app](#app)
    - [lib](#lib)
    - [validation](#validation)
    - [Weitere Module](#weitere-module)
  - [Formatierung und Linter](#formatierung-und-linter)
    - [Code Checks](#code-checks)
    - [Code formatieren](#code-formatieren)
  - [Tests ausführen](#tests-ausführen)

## Installation

### Python installieren

Stellen Sie sicher, dass Python auf Ihrem System installiert ist. Sie können die neueste Version von [python.org](https://www.python.org/downloads/) herunterladen und installieren.

### Virtuelle Umgebung erstellen

Erstellen Sie eine virtuelle Umgebung mit `venv`:

```sh
python -m venv venv
```

### Virtuelle Umgebung aktivieren

Aktivieren Sie die virtuelle Umgebung:

- Auf Windows:

```sh
venv\Scripts\activate
```

- Auf Unix oder MacOS:

```sh
source venv/bin/activate
```

### Abhängigkeiten installieren

Installieren Sie die Abhängigkeiten aus der `requirements.txt`:

```sh
pip install -r requirements.txt
```

### Server starten

Starten Sie den Entwicklungsserver:

```sh
python manage.py runserver
```

Der Server sollte nun unter `http://127.0.0.1:8000/` erreichbar sein.

## Entwicklung in VSCode

### Extensions

- Ruff: https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff

- Python: https://marketplace.visualstudio.com/items?itemName=ms-python.python

### Python Interpreter einstellen

Um den Python-Interpreter in VSCode einzustellen, folgen Sie diesen Schritten:

1. Öffnen Sie die Kommando-Palette mit `Ctrl+Shift+P` (Windows) oder `Cmd+Shift+P` (Mac).
2. Geben Sie `Python: Select Interpreter` ein und wählen Sie diese Option aus.
3. Wählen Sie den Interpreter aus, der sich in Ihrer virtuellen Umgebung befindet (`venv`).

Dies stellt sicher, dass VSCode die richtige Python-Version und die installierten Pakete in Ihrer virtuellen Umgebung verwendet.

## Projektstruktur

Eine Übersicht über die Projektverzeichnisstruktur und eine kurze Beschreibung der wichtigsten Ordner und Dateien.

### app

Das Verzeichnis `app` enthält die Hauptanwendung und die Routen für das FastAPI-Projekt. Hier sind die wichtigsten Komponenten und deren Funktionen:

- `main.py`: Der Einstiegspunkt der Anwendung. Hier wird die FastAPI-Instanz erstellt und die Routen werden registriert.
- `routes.py`: Hier sind die verschiedenen Router-Module registriert, die die Endpunkte der API definieren.
- `api/`: Hier sind die Geschäftslogik und die Service-Funktionen implementiert, die von den Routern verwendet werden.
- `static/`: Hier befinden sich statische Dateien, wie z.B. Bilder usw.
- `utils/`: Hier sind Hilfsfunktionen der Anwendung zu finden.
- `core/`: Dieses Verzeichnis enthält die Konfigurationsdateien.
- `media/`: Erstellte Medien durch die Anwendung, gehört nicht ins Repo.

Diese Struktur hilft dabei, den Code sauber und modular zu halten, was die Wartung und Erweiterung der Anwendung erleichtert.

### lib

Das Verzeichnis `lib` enthält allgemeine Bibliotheksfunktionen und Hilfsprogramme, die in verschiedenen Teilen der Anwendung verwendet werden können. Diese Funktionen sind oft wiederverwendbar und abstrahieren komplexe Logik, um sie einfacher zugänglich zu machen.

### validation

Das Verzeichnis `validation` enthält alle Validierungskomponenten der Anwendung.

### Weitere Module

Weitere Module können auf ähnliche Weise hinzugefügt werden, indem Sie neue Verzeichnisse und Dateien erstellen, die spezifische Funktionen und Logik kapseln. Hier ist ein Beispiel, wie Sie neue Module strukturieren können:

- `db/`: Hier könnten Datenbankverbindungen und ORM-Modelle definiert werden, um den Datenbankzugriff zu verwalten.

Durch das Hinzufügen neuer Module auf diese Weise bleibt die Codebasis organisiert und modular, was die Wartung und Erweiterung der Anwendung erleichtert.

## Formatierung und Linter

### Code Checks

```sh
python manage.py check
```

### Code formatieren

```sh
python manage.py format
```

## Tests ausführen

```sh
python manage.py test
```
