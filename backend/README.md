# HandScanAI Backend

## Inhaltsverzeichnis

- [HandScanAI Backend](#handscanai-backend)
  - [Inhaltsverzeichnis](#inhaltsverzeichnis)
  - [Installation mit Docker und Dev Container](#installation-mit-docker-und-dev-container)
    - [Schritte zur Installation](#schritte-zur-installation)
  - [Installation Ohne Docker](#installation-ohne-docker)
    - [MongoDB installieren](#mongodb-installieren)
      - [MongoDB mit Docker Compose starten](#mongodb-mit-docker-compose-starten)
      - [MongoDB manuell installieren](#mongodb-manuell-installieren)
    - [Python installieren](#python-installieren)
    - [Enviroment Datei erstellen](#enviroment-datei-erstellen)
    - [Virtuelle Umgebung erstellen](#virtuelle-umgebung-erstellen)
    - [Virtuelle Umgebung aktivieren](#virtuelle-umgebung-aktivieren)
    - [Abhängigkeiten installieren](#abhängigkeiten-installieren)
    - [Server starten](#server-starten)
  - [Setup](#setup)
    - [setup media](#setup-media)
    - [setup logging](#setup-logging)
  - [Developing in VSCode](#developing-in-vscode)
    - [Extensions](#extensions)
    - [Python Interpreter einstellen](#python-interpreter-einstellen)
  - [Projektstruktur](#projektstruktur)
    - [app](#app)
    - [classifier](#classifier)
    - [embeddings](#embeddings)
    - [hand-normalization](#hand-normalization)
    - [lib](#lib)
    - [logs](#logs)
    - [pipelines](#pipelines)
    - [tests](#tests)
    - [utils](#utils)
    - [validation](#validation)
    - [vectordb](#vectordb)
    - [Weitere Module](#weitere-module)
  - [Formatting and Linter](#formatting-and-linter)
    - [Code Checks](#code-checks)
    - [Code formatting](#code-formatting)
  - [Run tests](#run-tests)
  - [Backups erstellen und wiederherstellen](#backups-erstellen-und-wiederherstellen)
    - [Backup erstellen](#backup-erstellen)
    - [Backup wiederherstellen](#backup-wiederherstellen)

## Installation mit Docker und Dev Container

### Schritte zur Installation

**1. Docker Desktop installieren**: Laden Sie Docker Desktop von der [offiziellen Website](https://www.docker.com/products/docker-desktop) herunter und installieren Sie es.

**2. Dev Container VSCode Extension installieren**: Installieren Sie die Dev Container Extension in Visual Studio Code. Diese Erweiterung ermöglicht es Ihnen, Entwicklungscontainer zu verwenden.

**3. Im Container entwickeln**: Um im Container entwickeln zu können, öffnen Sie den Backend-Ordner als eigenes Fenster, dann bekommen Sie einen Popup "Reopen in Container", falls nicht dann mit `STRG + UMSCHALT + P` `Dev Container: Reopen in container`. Der Container wird gebaut und VSCode wird automatisch mit Einstellungen und Extensions entprechend der `devcontainer.json` konfiguriert.

Alternativ können Sie mit dem folgenden Befehl das Projekt starten:

```sh
docker-compose up
```

Falls ein Zugriff auf das Terminal des Containers gewünscht ist, dann führen Sie folgenden Befehl in einem Terminal aus:

```sh
docker exec -it backend /bin/bash
```

**4. Zugriff auf den Server**: Der Server sollte nun automatisch unter `http://127.0.0.1:8000` erreichbar sein.

## Installation Ohne Docker

### MongoDB installieren

#### MongoDB mit Docker Compose starten

Um MongoDB mit Docker zu starten, verwenden Sie den folgenden Befehl:

```sh
docker-compose up mongodb
```

Dieser Befehl startet den MongoDB-Dienst, wie er in der docker-compose.yml-Datei definiert ist.

#### MongoDB manuell installieren

Alternativ können Sie die offizielle Anleitung zur Installation der MongoDB-Community-Edition befolgen. Die Anleitung finden Sie hier:
[MongoDB Community Edition installieren](https://www.mongodb.com/docs/manual/administration/install-community/)

### Python installieren

Stellen Sie sicher, dass Python auf Ihrem System installiert ist. Sie können die neueste Version von [python.org](https://www.python.org/downloads/) herunterladen und installieren.

### Enviroment Datei erstellen

Die Datei `.env.sample` duplizieren und umbenennen in `.env`
Falls nötig, die Attribute in der Datei entsprechend der Konfiguration anpassen.

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

## Setup

Setup necessary to use the application. Describes creation of folder structures and base data.

### setup media

Create `backend/app/media` and inside

- `BaseImages`: contains all images of BaseDataset
- `csv`: contains Metadata.csv and {region}\_Embeddings.csv (created via `manage.py setup_new_project_data`, see `manage.py` docstrings for further information. Important: Create embedding-csvs new on every new computer/ don't copy them between devices.)
- `QueryImages`: place where images from frontend are saved
- `RegionImages`: results of hand-normalization

### setup logging

The `logs-folder` in `backend` and its contents are automatically created when starting the docker container (via `startup()` in `lifetime.py`). The log-csvs lie in a folder named after the current date to make distinctions between sessions easier.

To manually set up the correct logging file structure (in case of an error or development outside of docker), in the commandline use

```sh
python manage.py setup_csv_logging
```

## Developing in VSCode

### Extensions

- Ruff: <https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff>

- Python: <https://marketplace.visualstudio.com/items?itemName=ms-python.python>

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
- `lifetime.py`: Hier werden Funktionen definiert, die beim Starten und Beenden der Anwendung ausgeführt werden.
- `api/`: Hier sind die Geschäftslogik und die Service-Funktionen implementiert, die von den Routern verwendet werden.
- `static/`: Hier befinden sich statische Dateien, wie z.B. Bilder usw.
- `core/`: Dieses Verzeichnis enthält die Konfigurationsdateien.
- `db/`: Dieses Verzeichnis ist für die Datenhaltung zuständig.
- `media/`: Erstellte Medien durch die Anwendung, gehört nicht ins Repo.

Diese Struktur hilft dabei, den Code sauber und modular zu halten, was die Wartung und Erweiterung der Anwendung erleichtert.

### classifier

The ‘classifier’ directory contains the modules that are used to classify the age and gender of the results of the nearest neighbours. There are weighted and unweighted classifications. See the classifier-Readme for further information.

### embeddings

The directory `embeddings` contains the modules that are used for embeddings calculation via CNNs. Those embeddings are later used to determine similarities between images. See the embeddings-Readme for further information.

### hand-normalization

TODO

### lib

Das Verzeichnis `lib` enthält allgemeine Bibliotheksfunktionen und Hilfsprogramme, die in verschiedenen Teilen der Anwendung verwendet werden können. Diese Funktionen sind oft wiederverwendbar und abstrahieren komplexe Logik, um sie einfacher zugänglich zu machen.

### logs

The directory `logs` is not committed to the repo but is needed to store csv-files that are used to collect various data. It gets created automatically upon starting the backend docker container or has to be setup manually. For further information, see [Setup](#setup).

### pipelines

TODO

### tests

Das Verzeichnis `tests` enthält die Unit- und Integrationstests des Backends, die mittels `pytest` implementiert wurden. Es enthält eine eigene Readme für weitere Informationen.

### utils

The directory `utils` contains several modules with helper functions that are useful all across the app (e.g. enums used as dict-keys or functions to save data in csv-files). See utils' Readme for further details.

### validation

Das Verzeichnis `validation` enthält alle Validierungskomponenten der Anwendung.

### vectordb

TODO

### Weitere Module

Weitere Module können auf ähnliche Weise hinzugefügt werden, indem Sie neue Verzeichnisse und Dateien erstellen, die spezifische Funktionen und Logik kapseln. Hier ist ein Beispiel, wie Sie neue Module strukturieren können:

- `db/`: Hier könnten Datenbankverbindungen und ORM-Modelle definiert werden, um den Datenbankzugriff zu verwalten.

Durch das Hinzufügen neuer Module auf diese Weise bleibt die Codebasis organisiert und modular, was die Wartung und Erweiterung der Anwendung erleichtert.

## Formatting and Linter

### Code Checks

```sh
python manage.py check
```

### Code formatting

```sh
python manage.py format
```

## Run tests

```sh
python manage.py test
```

See also Readme in `tests`-module.

## Backups erstellen und wiederherstellen

### Backup erstellen

Um ein Backup der Ordner `volumes`, `logs` und `app/media` zu erstellen, führen Sie den folgenden Befehl aus:

```sh
python manage.py create_backup
```

Das Backup wird im Ordner backup erstellt und der Dateiname enthält das aktuelle Datum und die Uhrzeit.

### Backup wiederherstellen

Um ein Backup wiederherzustellen, muss die Datei unter dem Ordner `backup` stehen. Danach führen Sie den folgenden Befehl aus und geben Sie den Namen der Backup-Datei an:

```sh
python manage.py restore_backup <backup_datei>
```

**!!Hinweis!!**: Alle vorhandene Daten werden gelöscht und überschrieben, damit keinen Konflikt zwischen Vorhandenen Daten entsteht!
