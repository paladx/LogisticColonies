> Historisches Dokument zum Stand 0.3.x. Für den zentralen Warenfluss, die mitgelieferten Baupläne und den Build gilt die README von 0.5.0-dev.

# Structurize Tag Tool – LogisticColonies

**Bitte zuerst lesen:** Diese Tags sind *positionsgebundene Schematic-Tags* aus dem **Structurize Tag Tool**. Sie sind **keine** Minecraft-Blocktags, weshalb sie nicht unter `data/.../tags/block` registriert werden.

## Tag-Namen für die fünf Gebäudestufen

| Gebäudestufe | Bahnhof (am Little-Logistics-Docking-Station-Block) | Hafen (am Little-Logistics-Docking-Station-Block) | Zugehöriger Inventarblock |
|---|---|---|---|
| 1 | `gleis1` | `schiffsdock1` | `lager1` |
| 2 | `gleis2` | `schiffsdock2` | `lager2` |
| 3 | `gleis3` | `schiffsdock3` | `lager3` |
| 4 | `gleis4` | `schiffsdock4` | `lager4` |
| 5 | `gleis5` | `schiffsdock5` | `lager5` |

Alternativ zu `gleisN` bzw. `schiffsdockN` wird **`dockstationN`** erkannt – sinnvoll bei universellen Bauplänen. Vorrang hat immer das gebäudespezifische Tag. `lagerN` markiert einen Block mit einem NeoForge-ItemHandler (z.B. MineColonies-Rack), nicht irgendeinen dekorativen Kistenblock. Jeder Dockplatz braucht **ein vollständiges Paar**. Wenn mehrere Docks dasselbe Lager verwenden sollen, darf derselbe Lagerblock mehrere `lagerN`-Tags tragen; dasselbe Dock darf dagegen nicht mehreren Plätzen zugewiesen werden. Es sind maximal fünf Paare und maximal so viele gleichzeitig nutzbar, wie die aktuelle Gebäudestufe und die Zahl der Dockarbeiter erlauben.

**Wichtig:** Tags an Rails oder Wasserflächen dienen **nicht** als Dockposition. Das Tag muss **auf dem tatsächlichen Docking-Station-Block von Little Logistics** sitzen. Andernfalls meldet `tags inspect` einen ungültigen Dockblock.

## So werden die Tags im fertigen Schematic gespeichert

1. HUT-Block des gewünschten Gebäudes platzieren und das Bauwerk mit den Dock- und Lagerblöcken errichten.
2. Mit dem **Tag Tool** **Shift + Rechtsklick auf den HUT-Block**, damit dieser als **Anchor** ausgewählt ist.
3. Tag Tool mit Rechtsklick in die Luft öffnen und z. B. `gleis1` eingeben.
4. Den betreffenden Little-Logistics-Docking-Station-Block mit Linksklick markieren.
5. Als nächstes `lager1` eingeben und den passenden Lagerblock markieren. Für Stufe 2 `gleis2`/`lager2` usw. ergänzen.
6. Den Bauplan mit dem Scan Tool **mit demselben HUT-Anchor** speichern. Die Markierungen werden im Blueprint mitgespeichert.
7. Bei jedem weiteren Gebäude-Level die bereits vorhandenen Tags beibehalten und ein neues Paar pro Stufe ergänzen.

## Automatische Erkennung

Nach dem Bau (Level >= 1) liest LogisticColonies regelmäßig `IBuilding.getLocationsFromTag()` aus der MineColonies-Hütte und sucht die zugehörigen Dock/Lager-Paare. Wenn **noch kein manueller Link** existiert, werden gültige Paare automatisch verknüpft. Wenn ein Link bereits von Tag Tool gesteuert wird, aktualisiert er sich nach dem Ausbau (alle ca. 5 Sekunden). Ohne gültiges Paar bleibt eine bestehende Verknüpfung unverändert. Automatisch erkannte Plätze werden bei vorübergehend weniger gültigen Paaren nicht gelöscht; um eine absichtlich reduzierte Tag-Liste zu übernehmen, `tags sync` ausführen. Ungeladene Chunks werden nicht erzwungen geladen.

**Manuell verknüpfte Gebäude werden nicht verändert.** Willst du ein bestehendes Gebäude auf Schematic-Tags umstellen, führe `/logisticcolonies tags sync <x y z>` aus. Der Export-/Importmodus und konfigurierte Routen bleiben dabei erhalten.

## Befehle (OP-Level 2)

- `/logisticcolonies tags inspect <x y z>`: Zeigt erkannte Paare und Fehler, ohne Daten zu verändern.
- `/logisticcolonies tags sync <x y z>`: Übernimmt Markierungen und schaltet automatische Updates ein.
- `/logisticcolonies tags manual <x y z>`: Schaltet automatische Updates ab; bisherige Verbindungen bleiben bestehen.
- `/logisticcolonies status <x y z>`: Zeigt auch an, ob Dockverknüpfungen vom Tag Tool oder manuell stammen.

Die Befehle verwenden die **HUT-Koordinaten**. Diese Befehle wirken nur in bereits fertig gebauten Kolonien. Der Fahrplan und die Fahrzeugsteuerung bleiben Aufgabe von Little Logistics.

## Einschränkungen des Prototyps

- Noch keine Schematic-Dateien enthalten. Im Spiel müssen eigene fünf Varianten pro Gebäude angelegt und gespeichert werden.
- Tag-Erkennung wurde im Source implementiert, aber noch **nicht mit einem vollständigen NeoForge-Build und in einer Spielwelt getestet**.
- Das Logistikzentrum braucht für die vorhandene Funktion zunächst keine Positions-Tags. Später können `controller1` bis `controller3` für konkrete AI-Arbeitsplätze ergänzt werden, wenn eine Wegfindungs-AI implementiert wird.
- Das komplette Entfernen eines taggesteuerten Links führt bei verbleibenden Tags zur automatischen Neuanlage. Für dauerhafte Deaktivierung erst `tags manual` verwenden und die Tags im Schematic ändern.
