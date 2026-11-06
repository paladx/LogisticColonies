> Historisches Dokument zum Stand 0.3.x. Für den zentralen Warenfluss, die mitgelieferten Baupläne und den Build gilt die README von 0.5.0-dev.

# Fehlerbehebung: Invalid Timestamp bei :processResources

Der Fehler `Invalid Timestamp -2147483648000` betrifft Dateisystem-Zeitstempel in
`src/main/resources`, insbesondere bei entpackten Verzeichnissen wie `blockstates`.
Die Java-Kompilierung ist davon unabhängig.

## Bereits entpacktes Projekt reparieren (Linux / macOS)

Im Projektverzeichnis ausführen:

```bash
find src/main/resources -exec touch {} +
./gradlew clean build
```

Der Befehl setzt die Änderungszeit aller Dateien und Ordner unterhalb des
Ressourcenverzeichnisses auf die aktuelle Zeit.

## Neue Archivversion

Dieses ZIP enthält explizite Einträge für sämtliche Unterordner und gültige
ZIP-Änderungszeiten (2026-11-03). Damit sollten die Verzeichnismetadaten bei
üblichen ZIP-Entpackern korrekt ankommen. Die Java-Logik ist unverändert.

Hinweis: Die Mod wurde mit dieser Änderung nicht als kompletter Gradle-Build
getestet. Eventuell müssen weitere, unabhängige Fehler behoben werden.
