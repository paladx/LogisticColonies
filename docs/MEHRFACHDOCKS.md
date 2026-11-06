> Historisches Dokument zum Stand 0.3.x. Für den zentralen Warenfluss, die mitgelieferten Baupläne und den Build gilt die README von 0.5.0-dev.

# LogisticColonies: Mehrfach-Docks und Gebäudestufen (Entwurf 0.2.0-dev)

Alle drei MineColonies-Gebäude besitzen `getMaxBuildingLevel() == 5`.
Die Kapazität von Hafen/Bahnhof wird in `BuildingTiers` begrenzt.

| Level | Docking-Station-Verknüpfungen | Personal für Vollauslastung |
|:---:|:---:|:---:|
| 1 | 1 | 1 |
| 2 | 2 | 2 |
| 3 | 3 | 3 |
| 4 | 4 | 4 |
| 5 | 5 | 5 |

Pro Level 1 aktives Little-Logistics-Fahrzeug je Dock, jeder Liegeplatz bzw. Gleis benötigt
sein eigenes `DockingStationBlockEntity` und einen eigenen `IItemHandler` (Lager).
Ein Dock kann weder mehrfach im selben Gebäude noch bei einem anderen Gebäude registriert werden.

Alle ausgewählten Docks werden in einer Server-Tick-Runde einmal durchgegangen.
Bei Personalmangel wird die Auswahl je Tick-Runde rotiert; leere Liegeplätze
belegen keine Arbeiter. Die MineColonies-
Request-Token-Reservierungen werden pro Quellgebäude geteilt. Exportbedarfe stammen in
0.2.0-dev nur aus der Spieler-Fallback-Warteschlange von MineColonies; das ist noch kein
vollständiger MineColonies-Request-Resolver.

Unbekannte bzw. fehlende Docking-Stationen und Inventare werden übergangen. Ein Dock ohne
angedocktes Fahrzeug wird nicht verarbeitet. Bei Abbruch werden unvollständig zurückgegebene
Items als ItemEntity in der Spielwelt erhalten.

Das Logistikzentrum erhält 1, 2, 2, 3, 3 Controllerplätze über die Level 1–5.

## Implementierungsgrenzen

- Bisher keine automatisch erstellten physikalischen Hafen-/Bahnhof-Gleise und -Kaianlagen.
- Noch keine Structurize-Blaupausen (5× Hafen, 5× Bahnhof, 5× Logistikzentrum).
- Noch keine Client-GUI zur Dockverwaltung; OP-Kommandos sind die Konfigurationsoberfläche.
- Mehrere Docks eines Gebäudes teilen sich die Import/Export-Richtung und die Zielroute.
- Diese Projektversion muss noch mit Minecraft/NeoForge als JAR kompiliert und getestet werden.


## Neues in 0.2.4: Schematic-Tags

Tags für fünf Gleise bzw. Schiffsdocks und zugehörige Lager werden vom
Structurize Tag Tool automatisch übernommen. Details und Befehlshilfe:
[SCHEMATIC-TAGS.md](SCHEMATIC-TAGS.md).
