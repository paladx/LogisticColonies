# Tankwart, Tankstellen und Controller-Verkehrskoordination — 0.5.0-dev

## Neue Gebäude und neuer Beruf

Es gibt einen neuen MineColonies-Beruf **Tankwart** (`fuel_attendant`) und zwei
getrennte Hütten mit eigenen Items, Rezepten und MineColonies-BlockEntities:

- `logisticcolonies:ship_fuel_station`: Schiffstankstelle mit Wasserbecken und Schiffs-Docks.
- `logisticcolonies:rail_fuel_station`: Zugtankstelle mit Gleisen und Zug-Docks.

Beide gehören zum Baustil **LogisticColonies Industrial**. Jede Tankstelle besitzt
fünf eigene Baupläne. Die bisherigen drei Gebäude bleiben enthalten; insgesamt
enthält das Paket nun **25 Blueprints**. Dockpositionen und Hüttenanker bleiben
beim Ausbau bestehen. Fahrzeuge und der Anschluss an Wasserwege/Streckennetze
werden wie bisher in Little Logistics eingerichtet.

| Stufe | Tankplätze je Tankstelle | Tankwarte für volle Auslastung |
|---|---:|---:|
| 1 | 1 | 1 |
| 2 | 2 | 2 |
| 3 | 3 | 3 |
| 4 | 4 | 4 |
| 5 | 5 | 5 |

Ein Tankwart bedient einen belegten Tankplatz pro Sekundenzyklus. Bei zu wenig
Personal rotieren die Einsätze zwischen geeigneten belegten Tankplätzen.
Die Tankstellen beschäftigen Tankwarte, nicht Dockarbeiter.

## Was der Tankwart tatsächlich macht

1. Prüft, ob eine passende **Dampflok** beziehungsweise ein **Dampfschlepper**
   an der verknüpften Little-Logistics-Docking-Station liegt.
2. Verwendet das echte Motor-Brennstoffinventar des Fahrzeugs.
3. Überträgt bis zu **16 Brennstoffgegenstände pro Tankplatz und 20 Ticks**.
4. Nutzt zuerst den Tankplatzpuffer, dann das Hütteninventar und anschließend
   ein verfügbares, mit Controller besetztes Zentrallager derselben Kolonie.
5. Informiert die Docking-Station über erfolgte Transfers, damit die normale
   Little-Logistics-Aufenthaltslogik den Ladevorgang berücksichtigen kann.

Die Zulässigkeit eines Gegenstands bestimmt der native Little-Logistics-
`FuelItemStackHandler`. Kohle und andere vom Motor akzeptierte Ofenbrennstoffe
werden in den Motor gegeben. Fracht wird dabei nicht als Brennstoffinventar
verwendet. Schiffstankstellen bedienen keine Lokomotiven und Zugtankstellen
keine Schlepper. Bargen und Waggons ohne eigenen Dampfmotor werden nicht betankt.

**Elektroloks und Elektroschlepper werden in dieser Fassung nicht geladen.**
Es gibt keine neu eingeführten Flüssigtreibstoffe und keinen eigenen Flüssigkeitstank.
Der Begriff Tankstelle bezeichnet hier die Versorgung der vorhandenen Dampfmotoren
mit ihren von Little Logistics unterstützten Gegenstandsbrennstoffen.

Die Betankung wird serverseitig ausgeführt. Die Arbeitsplatz-AI geht zur Hütte;
der NPC trägt den Brennstoff noch nicht sichtbar zum Motor. Wie bei den bisherigen
Berufen zählt die Anstellung; Anwesenheit, Arbeitszeiten und Erfahrung beeinflussen
den Transfer derzeit nicht.

## Brennstoff über MineColonies anfordern

Wenn im Hütteninventar und in den aktiven lokalen Tankpuffern kein geeigneter
Brennstoff liegt, kann die besetzte Tankstelle alle zehn Sekunden eine native
Gebäudeanforderung über **64 Kohle** erstellen. Bereits offene Gebäude-/Bürger-
Anforderungen unterdrücken eine erneute Anforderung. Der normale MineColonies-
Resolver und die Kuriere liefern in das Hütteninventar.

Eine Anfrage erzeugt keine Gegenstände. Ist keine Kohle verfügbar, bleibt die
Anforderung im normalen Request-System offen. Andere akzeptierte Brennstoffe
können manuell oder durch Create/AE2 in die Puffer eingespeist werden; die
automatische Standardanforderung verlangt ausdrücklich Kohle.

Die Tankstelle kann auch ohne Logistikzentrum aus ihren lokalen Vorräten arbeiten.
Nur der zusätzliche Zugriff auf das Zentrallager benötigt ein betriebenes Zentrum.

## Tags und Einrichtung der Tankplätze

Die neuen Blueprints enthalten bereits passende positionierte Structurize-Tags:

| Gebäude/Zweck | Tags |
|---|---|
| Schiffs-Tankdock | `tankschiff1` … `tankschiff5` |
| Zug-Tankdock | `tankgleis1` … `tankgleis5` |
| Alternative Dockmarkierung | `dockstation1` … `dockstation5` |
| Brennstoffpuffer | `treibstofflager1` … `treibstofflager5` |
| Alternativer Puffername | `lager1` … `lager5` |

Docktags müssen auf den **unteren Controllerblock** der Docking-Station zeigen,
Puffertags auf ein zugängliches Inventar. Nummern lückenlos ab 1 vergeben und pro
Nummer genau ein Dock-/Lagerpaar verwenden. Über das Tag-/Scan-Tool mit dem
Hüttenanker speichern. Bestehende manuelle Links werden nicht ungefragt überschrieben.

```mcfunction
/logisticcolonies tags inspect <tankstellenhuette_x y z>
/logisticcolonies tags sync <tankstellenhuette_x y z>
/logisticcolonies status <tankstellenhuette_x y z>
/logisticcolonies link <tankstellenhuette_x y z> <dock_x y z> <brennstoffpuffer_x y z>
```

Tankstellen haben keinen Fracht-Import-/Exportmodus und keine Fracht-Zielroute.
Die vorhandenen `mode`, `send` und `route`-Befehle bleiben auf Frachtgebäude beschränkt.
Im Little-Logistics-Fahrplan muss das Fahrzeug die Tankstelle tatsächlich anfahren;
eine automatische Umplanung zur nächsten Tankstelle ist noch nicht enthalten.

## Der Controller als Verkehrskoordinator

Der Controller verwaltet jetzt zusätzlich **exklusive Verkehrsabschnitte**.
Ein Abschnitt ist ein frei benannter Quader in einer Dimension, beispielsweise
über einer Kreuzung, einem eingleisigen Engpass oder einer schmalen Hafeneinfahrt.
Züge und Schiffe verwenden dieselbe Reservierungslogik, wenn sie denselben Abschnitt
berühren. Unterschiedliche Stockwerke lassen sich durch passende Höhenbereiche trennen.

Ein fertig gebautes Logistikzentrum kann **einen Abschnitt je Gebäudestufe**
verwalten: Stufe 1 einen Abschnitt, Stufe 5 fünf Abschnitte. Ein angestellter
Controller genügt zur Betriebsfreigabe. Zusätzliche Controller steigern die
Verkehrsleistung aktuell nicht separat. Bei Herabstufung werden nur die ersten
Abschnitte in alphabetischer Reihenfolge bis zur aktuellen Stufengrenze neu freigegeben;
bestehende Belegungen bleiben geschützt.

Das Zentrum benötigt für die Verkehrsaufgabe kein Zentrallager. Für neue Einfahrten
müssen das Zentrum besetzt und der gesamte Abschnitt geladen sein.

### Einrichtung

```mcfunction
/logisticcolonies traffic zone <zentrum_x y z> <name> <erste_ecke_x y z> <zweite_ecke_x y z>
/logisticcolonies traffic status
```

Die Ecken markieren den **gesamten Konfliktbereich einschließlich aller gefährlichen
Kurven und Kreuzungsarme**, nicht nur einen einzelnen Schienenblock. Die Höhe muss
die Fahrzeugkörper umfassen. Die Einrichtung erfordert OP-Level 2.

- Namen: 1–48 Buchstaben, Ziffern, Unterstriche oder Bindestriche; Präfix `tag_` ist reserviert.
- Maximale Größe: 256 × 64 × 256 Blöcke.
- Abschnitte dürfen sich nicht überschneiden. Einen zusammenhängenden Engpass besser
  als einen Abschnitt definieren statt in viele unmittelbar benachbarte Abschnitte zu zerlegen.
- Bei der Einrichtung müssen Abschnitt und Vorfeld geladen sein.
- Der Controller betrachtet ein konservatives **12-Block-Vorfeld** in horizontaler
  Richtung, zusätzlich zu Fahrzeugkörper und Sicherheitsrand. Fahrzeugbewegung fließt
  über eine vorausberechnete Hüllfläche ein. Parkplätze, parallele Strecken und
  Ausweichstellen sollten außerhalb dieses Vorfelds liegen, sonst können auch dort
  stehende Fahrzeuge den Abschnitt reservieren oder angehalten werden.

### Ablauf

1. Vor jedem Server-Tick werden geladene Little-Logistics-Fahrzeuge erfasst.
2. Verbundene Wagen und Bargen werden als Verband behandelt. Erwartete Mitglieder
   aus Little Logistics' gespeicherter Zug-/Konvoiliste werden ebenfalls berücksichtigt.
3. Ein Fahrzeugverband fordert die berührten beziehungsweise nahegelegenen Abschnitte an.
4. Die zuerst beobachtete Warteschlange erhält Vorrang; bei gleichem Zeitpunkt entscheidet
   eine stabile UUID-Reihenfolge. Ein Verband erhält alle gerade angeforderten Abschnitte
   gemeinsam oder wartet, ohne davon nur einen Teil neu zu reservieren.
5. Wartende Fahrzeugverbände werden **vor ihrem Entity-Tick** angehalten. Die Geschwindigkeit
   wird auf null gesetzt; der native Bewegungstick und die Kettenkorrektur werden für diesen
   Tick ausgesetzt. Motorzustand, Fahrplan und dauerhafte Frozen-Flags werden nicht geändert.
6. Wenn die Freigabe vorliegt, läuft der normale Little-Logistics-Tick wieder.
7. Die Reservierung endet erst, wenn alle bekannten Mitglieder geladen sind und der
   vollständige Verband Abschnitt und Vorfeld verlassen hat. Die Lok allein genügt nicht.

Fällt der Controller aus, werden neue Einfahrten gesperrt. Ein bereits im Abschnitt
befindlicher vollständiger Verband darf ihn räumen. Ein zuvor reserviertes, aber
noch nicht eingefahrenes Fahrzeug erhält ohne Controller keine neue Einfahrt.
Nach dem Snapshot neu geladene Fahrzeuge müssen im Vorfeld zunächst auf den nächsten
Snapshot warten.

### Neustart, entladene Chunks und Störungen

Abschnittsdefinitionen, reservierender Verband und bekannte Mitglieder werden in
`logisticcolonies_traffic_v1` mit NBT gespeichert. Es gibt **keine zeitgesteuerte
Freigabe** einer unbekannten Belegung. Fehlende/entladene Fahrzeuge behalten ihre
Reservierung. Die Verkehrssteuerung erzwingt keine Chunk-Ladung.

Sind beim Start oder nach einem Teleport mehrere unabhängige Verbände bereits in
einem Abschnitt, werden sie angehalten; der Status meldet **NOTHALT: Mehrfachbelegung**.
Die Steuerung wählt dann nicht willkürlich eines der Fahrzeuge zur Weiterfahrt aus.
Der Spieler muss den Konflikt räumen. Das System berechnet keine Rückwärtsfahrt,
Umleitung oder Rangierlösung.

Für eine verwaiste Reservierung bzw. eine nicht mehr benötigte Definition:

```mcfunction
/logisticcolonies traffic release <name>
/logisticcolonies traffic remove <name>
```

Diese Befehle benötigen OP-Level 4. Sie funktionieren nur, wenn Abschnitt und
Vorfeld vollständig geladen und nachweislich ohne Little-Logistics-Fahrzeuge sind.
`release` entfernt nur die Reservierung, `remove` auch die Abschnittsdefinition.
Keine der beiden Funktionen erteilt eine Freigabe durch eine noch belegte Stelle.

## Reichweite und verbleibende Grenzen

Die Erweiterung bietet Kollisionsvermeidung durch gegenseitigen Ausschluss in
**konfigurierten Abschnitten mit korrekt dimensionierten Vorfeldern**. Außerhalb
solcher Abschnitte bleiben die nativen Mechanismen von Little Logistics zuständig,
unter anderem dessen vorhandene Zug-Kollisionsprüfung und Weichenreservierungen.

Sie ist keine globale Kollisionsgarantie, kein vollständiger Fahrdienstleiter mit
Netzpfadsuche und keine Steuerung von Create-Zügen oder Vanilla-Minecarts.
Teleports, nachträglich in einen belegten Abschnitt gesetzte Fahrzeuge, fremde
Bewegungsänderungen oder falsch dimensionierte Abschnitte können Konflikte erzeugen.
Das Anhalten kann eine schon vorhandene räumliche Überlappung nicht rückgängig machen.
Ein ungünstig aufgebautes Netz kann blockieren; es gibt keine automatische Deadlock-Auflösung.

Die Mindestversion Little Logistics beta.2 ist weiterhin erforderlich. Ein kleines
read-only Mixin liest dessen gespeicherte Schiffskonvoi-Mitglieder, weil diese
Version dafür keine öffentliche Zugriffsmethode besitzt. Die Mod überschreibt
weder dessen Navigation noch Weichen- oder Signalzustände.
