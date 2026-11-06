# Prüfprotokoll — LogisticColonies 0.5.0-dev

Datum: 4. November 2026. Minecraft 1.21.1, Java 21, Gradle 8.14.3,
NeoForge 21.1.219, MineColonies 1.1.1403 und Little Logistics 1.21.1.1-beta.2.

## Ausgeführte Prüfungen

- Vollständiger Build mit JAR-Erzeugung und acht expliziten Java-Prüfprogrammen:
  BuildingTiers, BerthScheduler, LogisticsTagNames, ShipmentAccounting,
  RouteSecurity, DetachedReservations, LogisticsData und TrafficArbiter.
- TrafficArbiter prüft exklusive Einfahrt, FIFO-Vorrang, atomare Mehrbereichsvergabe,
  Verweigerung neuer Einfahrten ohne Controller, Ausfahrt eines vorhandenen Belegers,
  Controllerverlust vor der Einfahrt, Mehrfachbelegung/Notstopp und das Beibehalten
  von Reservierungen bei fehlendem Verband oder unvollständigem Zugschluss.
- `scripts/test-core.sh` führt die sieben Minecraft-unabhängigen Prüfläufe aus.
  Die achte Prüfung LogisticsData verwendet echte Minecraft-NBT-Typen und läuft im Build.
- `scripts/validate-blueprints.py`: 25/25 Baupläne mit vollständigen Dock-Multiblocks,
  Ankern, Paletten und zusammengehörigen Dock-/Lager-Tags. Beim Ausbau bleiben die
  bisherigen Dockpositionen bestehen. Pack-Metadaten und Symbol werden mitgeprüft.
- Dedicated-Server-Start zusammen mit Create 6.0.10, AE2 19.2.18, GuideME 21.1.22,
  CreateColony 1.0.0 und AE2Colonies 1.2.2. Der Server registriert
  `LogisticColonies Industrial`, startet die Testwelt, führt den Selbsttest aus,
  speichert die Welt und beendet sich geordnet.
- Der Server-Selbsttest liest alle **25 Blueprints** mit Structurize, instanziiert
  ihre Hütten-BlockEntities im Speicher, prüft deren Gültigkeit und die eingelesenen Tags.
- Native Brennstoffprüfung mit echten, nur im Speicher erzeugten Little-Logistics-
  Dampfloks und Dampfschleppern: 16 Kohle je Motor, keine Vermischung der Fahrzeugtypen,
  keine Annahme von Erde als Treibstoff und Erhaltung der übertragenen Stückzahlen.
- Laufzeitprüfung des NBT-Rundlaufs für Verkehrsabschnitte und Verband-Reservierungen.
  Eine fehlende Lok und ein fehlendes Anhängefahrzeug führen nicht zu einer TTL-Freigabe.
- Laufzeitprüfung der EntityTickEvent-Haltefunktion an echten LL-Zug-/Schiffsobjekten:
  vor dem Tick wird die Bewegung auf null gesetzt und das Event abgebrochen;
  nach Wegfall der Halteentscheidung wird der Tick wieder zugelassen.
- Das read-only Mixin für gespeicherte Schiffs-Konvoimitglieder wird auf dem Server
  geladen und durch einen tatsächlichen Zugriff geprüft.

Die Vehicle-Objekte der direkten Funktionsprüfungen werden nicht in die Welt
aufgenommen. Benutzerwelten und Spielerinventare werden nicht verändert.

## Reproduzieren

Die Abhängigkeiten entsprechend README/libs installieren. Für die Prüfung mit
CreateColony und AE2Colonies auch deren JARs und GuideME im Entwicklungs-Modordner
bereitstellen. Dann:

```sh
./gradlew build
./gradlew runServer -PlogisticcoloniesSelfTest
```

Den Testserver regulär einrichten. Seine EULA-Datei ist nicht im Quellpaket enthalten.
Der Selbsttest-Modus beendet den Server nach der Prüfung; ein normaler `runServer`
bleibt gestartet. In der Cloud wurde für den Dedicated-Server der Client-Asset-
Download ausgelassen, nicht die Kompilierung oder die fachlichen Prüfungen:

```sh
./gradlew build runServer -PlogisticcoloniesSelfTest \
  -x neoFormJoined1.21.1-20240808.144430DownloadAssets
```

Die bereinigten Konsolennachweise liegen in `validation/0.5.0-dev/`.
Verbindungswarnungen von Minecrafts Online-Schlüsselabfrage und dem Versionscheck
sind umgebungsbedingt; ein öffentlicher Online-Serverbetrieb wurde nicht geprüft.

## Grenzen der Nachweise

Der erfolgreiche Serverstart und die direkten Funktionsprüfungen ersetzen noch
keinen vollständigen Spieltest. Nicht nachgewiesen sind:

- Clientdarstellung, Bau- und Ausbauvorgänge mit echten Baumeister-NPCs und Anstellung.
- Die vollständige Kette aus Kohleanforderung, Kurierzustellung, Anfahrt und Betankung
  an einem real gebauten Tankstellendock.
- Reale Mehrfahrzeugfahrten durch ein aufgebautes Verkehrsnetz einschließlich
  Kreuzungen, Kurven, Chunkwechseln und langfristiger Konfliktauflösung.
- Funktionale Create-/AE2-Netzversorgung und das Zusammenspiel konkurrierender
  Resolver im laufenden Koloniespiel.

Die Verkehrslogik wurde anhand gezielter Zustandsfälle und der echten Tick-Sperre
geprüft. Es wird ausdrücklich keine globale Kollisionsfreiheit behauptet.
Der Schutz setzt eingerichtete, passend dimensionierte Verkehrsabschnitte voraus.
