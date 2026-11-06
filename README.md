# LogisticColonies 0.5.0-dev — NeoForge 1.21.1

MineColonies-Addon für physische Transporte mit Little Logistics. Dieser Entwicklungsstand
baut auf dem bereitgestellten Quellarchiv 0.3.0-dev auf. Die JAR und Quellen enthalten
keine fremden Mod-JARs. Der aktuelle Prüfstand steht in `docs/PRUEFPROTOKOLL.md`: Build, acht Build-Prüfungen
und Dedicated-Server-Selbsttest bestehen, auch beim gemeinsamen Start mit Create/AE2
und den beiden bereitgestellten Integrationsaddons. Fahrzeugfahrten, Kurier-Nachschub, reale Tankstellennutzung und Mehrfahrzeugverkehr
sind noch nicht durchgängig im Spiel geprüft.

## Neu in 0.5.0-dev

- Neuer Beruf **Tankwart** und zwei getrennte Hütten: **Schiffstankstelle** und **Zugtankstelle**.
- Beide Tankstellen sind bis Stufe 5 ausbaubar, mit 1–5 Tankplätzen und entsprechendem Personal.
- Betankung von Little-Logistics-Dampfloks und Dampfschleppern direkt im Motorinventar;
  bis 16 akzeptierte Brennstoffgegenstände pro Platz und Sekundenzyklus.
- Native Kohle-Anforderung über MineColonies bei leerem lokalen Brennstoffvorrat.
- Controller vergeben exklusive, persistente Verkehrsabschnitte und halten wartende
  vollständige Fahrzeugverbände vor deren Bewegungstick an.
- 25 Baupläne einschließlich zehn neuer Tankstellen-Blueprints, eigene HUT-Blöcke,
  Rezepte und positionierte Tags.

**Einrichtung, Befehle und Grenzen:** [Tankstellen und Verkehr](docs/TANKSTELLEN-UND-VERKEHR.md).
Der Verkehrsschutz wirkt in eingerichteten Abschnitten; er ersetzt keine globale
Netzplanung. Elektromotoren werden in dieser Fassung nicht geladen.

## Gebäude und Berufe

| Gebäude | Stufen | Kapazität |
|---|---|---|
| Schiffsdock / Hafen | 1–5 | 1–5 Docking-Stations, bis zu fünf Dockarbeiter |
| Zughaltestelle / Bahnhof | 1–5 | 1–5 Gleise mit Docking-Stations, bis zu fünf Dockarbeiter |
| Schiffstankstelle | 1–5 | 1–5 Tankplätze, bis zu fünf Tankwarte |
| Zugtankstelle | 1–5 | 1–5 Tankplätze, bis zu fünf Tankwarte |
| Logistikzentrum | 1–5 | 1/2/2/3/3 Controllerplätze; Lagerhausübergabe bis 64 × Stufe Items pro Sekunde |

Ein eigener Baustil **LogisticColonies Industrial** enthält 25 originale Structurize-Baupläne.
Die Position der Hütte und bestehender Docks bleibt beim Ausbau gleich. Die Entwürfe
sind einfache offene Industriehöfe mit Wetterschutz, Beleuchtung und Lagerfässern.
Hafen und Bahnhof erhalten pro Stufe genau einen zusätzlichen Dockplatz. Beim Zentrum
wachsen die Lagerfläche und die Zahl der Fässer. Das mit `zentrallager` markierte Fass
ist der aktive Warenpuffer; zusätzliche Fässer sind zunächst baulicher Lagerplatz.

Dockarbeiter, Tankwarte und Controller sind eigene MineColonies-Jobs mit Arbeitsplatz-AI.
Die Transfers erfolgen serverseitig. Es gibt keine animierte Beförderung einzelner Pakete
zwischen Hütte, Lager und Dock und keine Anwesenheits-/Arbeitszeitprüfung des NPCs;
entscheidend ist die Stellenbesetzung. Für die letzte Zustellung ist kein zusätzlicher Beruf nötig: Die letzte Zustellung übernehmen die vorhandenen MineColonies-Kuriere.

## Installation

Java 21, Minecraft **1.21.1**, NeoForge **21.1.219 oder neuer**.
Auf Client und Server dieselben Mod-Versionen installieren:

- LogisticColonies 0.5.0-dev
- MineColonies `1.1.1403-1.21.1`
- Little Logistics `1.21.1.1-beta.2`
- Structurize `1.0.835-1.21.1-snapshot`
- BlockUI `1.0.210-1.21.1-snapshot`
- Domum Ornamentum `1.0.236-snapshot`
- Multipiston `1.2.58-1.21.1`
- Little Logistics benötigt Ponder ab `1.0.82+mc1.21.1`; die bereitgestellte JAR
  bettet Ponder und Flywheel bereits ein.

Create und Applied Energistics 2 sind optional und benötigen ihre eigenen Abhängigkeiten.
Die beigefügten Mods **CreateColony** und **AE2Colonies** ersetzen Create bzw. AE2 nicht.
LogisticColonies verändert deren Klassen und Resolver nicht. Der gemeinsame Dedicated-Server-Start mit diesen Addons wurde erfolgreich geprüft;
die funktionale Zusammenarbeit der Logistiknetze benötigt weiterhin einen Spieltest.

## Warenfluss

```text
Import: Fahrzeug → Dockfass → Zentrallager → MineColonies-Lagerhaus → Kurier → Bedarf
Export: Lagerhaus oder extern befülltes Zentrallager → Zentrallager → Fahrzeug → Zielhafen
```

In jeder beteiligten Kolonie muss ein fertig gebautes Logistikzentrum mit mindestens
einem angestellten Controller und eingerichtetem Zentrallager vorhanden sein.
Import- und Exporthütten sind getrennte Modi. Ein Dockarbeiter bedient einen belegten
Dockplatz pro Zyklus. Bei Personalmangel rotieren die Arbeitsplätze fair.
Alle aktiven Plätze werden im selben Sekundenzyklus bedient, bis zu 64 Items je Dock.
Es werden keine Chunks erzwungen geladen.

Das Zentrallager wird beim eigenen Baustil über den Tag `zentrallager` automatisch
gefunden. Alternativ kann ein OP ein Inventar in derselben Kolonie verbinden:

```mcfunction
/logisticcolonies hub <zentrum_x y z> <lager_x y z>
/logisticcolonies status <zentrum_x y z>
```

Importe werden zuerst ins zentrale Inventar und danach in zugängliche Container
fertiger MineColonies-Lagerhäuser eingelagert. Der normale MineColonies-Request-Resolver
und die Kuriere übernehmen die Endzustellung. Ohne Lagerhaus oder bei Platzmangel
bleiben die Waren im Puffer. Exporte können benötigte Bestände aus Lagerhauscontainern
über das Zentrum zum Fahrzeug übernehmen. Der lokale Transfer ist eine serverseitige
Inventarbrücke, während die Reise zwischen den Haltepunkten physisch mit Little Logistics erfolgt.

## Erste Strecke

1. Eine Kolonie mit Lagerhaus und Kurier aufbauen. Logistikzentrum und Hafen/Bahnhof
   mit dem Build Tool aus **LogisticColonies Industrial** bauen; Personal einstellen.
2. Hafenbecken mit einem ausreichend tiefen Wasserweg beziehungsweise Bahnhofsgleise
   mit der Strecke verbinden. Fahrzeuge und Fahrpläne mit Little Logistics einrichten.
   Die Baupläne liefern Haltepunkte, kein vollständiges Streckennetz und keine Fahrzeuge.
3. In der Zielkolonie ebenfalls Zentrum, Lagerhaus, Kurier und Importhütte einrichten.
4. Die eingebetteten Tags werden alle fünf Sekunden geprüft. Status prüfen:

```mcfunction
/logisticcolonies tags inspect <quellhuette_x y z>
/logisticcolonies tags sync <quellhuette_x y z>
/logisticcolonies mode <quellhuette_x y z> export
/logisticcolonies mode <zielhuette_x y z> import
/logisticcolonies route <quellhuette_x y z> <zielhuette_x y z>
/logisticcolonies demands <zielhuette_x y z>
/logisticcolonies status <quellhuette_x y z>
```

Für jedes Dock ist auch ein eigenes Ziel möglich:

```mcfunction
/logisticcolonies route berth <quellhuette_x y z> 1 <zielhuette_x y z>
```

Die Inventare müssen Waren enthalten, die einer offenen unterstützten Anfrage der
Zielkolonie entsprechen. Ohne Bedarf erfolgt kein automatischer Export. Quelle und
Ziel müssen in derselben Dimension liegen. Standardmäßig müssen beide Kolonien
denselben Besitzer haben; die vorhandene gezielte Fremdkolonie-Freigabe erfordert OP-Level 4.
Alle übrigen Einrichtungsbefehle erfordern OP-Level 2.

## Scan-/Tag-Tool

Diese **positionsgebundenen Structurize-Tags** auf dem Bauplananker speichern:

| Zweck | Tags | Markierter Block |
|---|---|---|
| Schiffe | `schiffsdock1` … `schiffsdock5` | unterer Controller der Little-Logistics-Docking-Station |
| Züge | `gleis1` … `gleis5` | unterer Controller der Little-Logistics-Docking-Station |
| allgemeines Dock | `dockstation1` … `dockstation5` | alternativer Name für denselben Controller |
| Dockpuffer | `lager1` … `lager5` | zugehöriges Fass oder ItemHandler-Inventar |
| Zentrum | `zentrallager` | das aktive zentrale Inventar |

Mit dem Tag Tool markieren und zusammen mit dem Hüttenanker mit dem Scan Tool als
Blueprint speichern. Je Paar dieselbe Nummer verwenden und keine Tags doppelt vergeben.
Nicht die Brücke oder den oberen Dockteil markieren. Für einen eigenen Baustil ist
je Gebäudetyp eine zusammengehörige Serie `harbor1`…`harbor5`,
`railway_station1`…`railway_station5`, `logistics_center1`…`logistics_center5` notwendig.
Die eingebauten Baupläne enthalten diese Markierungen bereits.

Zusätzlich existieren Minecraft-Blocktags `logisticcolonies:docking_stations`,
`logisticcolonies:ship_docks`, `logisticcolonies:rail_stops`. Little Logistics verwendet
für Züge und Schiffe denselben Dockblock; diese Registry-Tags umfassen daher denselben
Block einschließlich seiner Multiblockteile. Sie ersetzen die positionsgebundenen
Tag-Tool-Markierungen nicht.

Manuelle Dockeinrichtung und Diagnose:

```mcfunction
/logisticcolonies link <huette_x y z> <dock_x y z> <dockfass_x y z>
/logisticcolonies tags manual <huette_x y z>
/logisticcolonies unlink <huette_x y z> <dock_x y z>
/logisticcolonies selftest
```

`selftest` prüft im geladenen Modpack Inventartransfer, Motorbetankung,
Verkehrsreservierungen, Tick-Haltefunktion und alle 25 Baupläne mit dem echten Structurize-Parser. Es werden dabei keine Weltblöcke
oder Spielerinventare verändert. `send` ist ein OP-Testbefehl für manuelle Verladung
aus dem Zentrum; er umgeht bewusst die automatische Request-Reservierung.

## Create und AE2

Die Anbindung verwendet NeoForge `IItemHandler`. Create kann Waren über Trichter,
Rutschen oder andere geeignete Übergaben in ein zentrales Fass einspeisen bzw.
abholen. Für AE2 eignen sich Import-/Export-Busse am zentralen Fass; ein zugängliches
Interface-/Pufferinventar kann ebenfalls verwendet werden. Die Konfiguration dieser
Netze bleibt bei Create/AE2. Die normale Fasslösung verlangt keine direkte API dieser Mods.

Es gibt **keine native Create-Stock-Link-Paketbestellung**, keinen Zugriff auf den
gesamten ME-Netzwerkbestand und kein von LogisticColonies gestartetes AE2-Autocrafting.
Create-Pakete werden als normale Gegenstände behandelt und nicht automatisch geöffnet.
Der derzeitige Transport bewegt ItemStacks, keine eigene adressierte Paketentität.

## Request-System und Grenzen

Es werden vorhandene native `IDeliverable`-Anfragen mit dem jeweiligen MineColonies-
Gegenstandsvergleich ausgelesen. Exportfähig sind Anforderungen beim Player-/Retrying-
Resolver; laufende Handwerker-/Kurieraufträge werden nicht zusätzlich übernommen.
LogisticColonies registriert keinen eigenen Request-Resolver und schließt keine
Anfrage vorzeitig ab. Bestandsänderungen stoßen die normale Neubewertung an.

Bereits verladenes Transportgut wird pro Request und Zielkolonie gemeinsam reserviert,
auch bei mehreren Exporthäfen. Das Versandbuch übersteht Neustart, Routenwechsel
und Entfernen des Quellgebäudes. Es gibt noch keine Fahrzeug-/Paketidentität zur
Lieferbestätigung: Verlorene Transporte werden deshalb nicht automatisch erneut
verschickt. Alte 0.2.x-Buchungen bleiben konservativ erhalten.

## Bauen und Prüfen

Die sechs Original-Pflicht-JARs aus `libs/README.md` nach `libs/` legen. Dann:

```sh
./gradlew build
# Windows: gradlew.bat build
```

Der Wrapper verwendet Gradle **8.14.3** mit SHA-256-Prüfung, passend zum verwendeten
NeoGradle 7.1.38. Ausgabe: `build/libs/logisticcolonies-0.5.0-dev.jar`.
Der Build führt acht explizite Java-Prüfprogramme aus; das Standard-JUnit-Task ist
deaktiviert, da diese Prüfungen Java-main-Programme sind. Inventar-, Brennstoff- und Verkehrsprüfungen mit Minecraft-
Registries laufen im geladenen Spiel über `selftest`.

```sh
bash scripts/test-core.sh
# Nur zum Regenerieren/Prüfen der bereits enthaltenen Blueprints:
python -m pip install nbtlib==2.0.4
python scripts/generate-blueprints.py
python scripts/validate-blueprints.py
./gradlew runClient
./gradlew runServer
```

Vorhandene Weltdaten werden weiter unter `logisticcolonies_network_v1` gelesen.
Alte Netzwerke müssen zusätzlich ein Zentrallager verbinden; danach ist der neue
zentrale Warenfluss aktiv. Nur das erste markierte Zentrum einer Kolonie wird
automatisch verbunden; `hub` kann die aktive Zuordnung explizit ersetzen.

## Lizenz

GPL-3.0-only entsprechend der vorhandenen Repository-Lizenz `LICENSE`.
Minecraft, MineColonies, Little Logistics und weitere Mods behalten ihre eigenen
Lizenzen. Sie sind nicht Bestandteil dieser Addon-JAR oder des Quellpakets.
