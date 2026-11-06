> Historisches Dokument zum Stand 0.3.x. Für den zentralen Warenfluss, die mitgelieferten Baupläne und den Build gilt die README von 0.5.0-dev.

# Fünf Ausbaustufen – Entwurf für späteres Structurize-Blueprintset

Diese Übersicht definiert Ausbaustufen, damit die 15 fehlenden MineColonies-Schematics
anschließend zur technischen Mehrfach-Dock-Funktion passen. Die in der Tabelle genannten
Strukturteile sind **Bauziele**, noch keine mitgelieferten Minecraft-Baupläne.

| Stufe | Hafen (Kapazität) | Bahnhof (Kapazität) | Logistikzentrum (Arbeitsplätze) |
|---|---|---|---|
| 1 | Kleiner Anleger, 1 Dock/Schiff | Einzelgleis, 1 Dock/Zug | Leitstand, 1 Controller |
| 2 | Erweiterter Kai, 2 Docks/Schiffe | Zweigleisiger Umschlag, 2 Docks/Züge | Büro und Disposition, 2 Controller |
| 3 | Mittlerer Hafen, 3 Docks/Schiffe | Güterbahnhof, 3 Docks/Züge | Lager-/Liefertafel, 2 Controller |
| 4 | Großer Güterhafen, 4 Docks/Schiffe | 4 Gleise, Verladebereich | Netzsteuerung, 3 Controller |
| 5 | Zentralhafen, 5 Docks/Schiffe | 5 Gleise, großer Umschlag | Zentrales Logistikzentrum, 3 Controller |

Jede physische Little-Logistics-Docking-Station muss nach dem Bau mit
`/logisticcolonies link <gebäude> <dock> <lager>` separat registriert werden.

Die derzeitige Umsetzung erzeugt keine zusätzlichen Docks bei einem Gebäude-Upgrade.
Docks und die entsprechenden Transportwege müssen vom Spieler separat aufgebaut werden.
