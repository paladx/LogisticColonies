> Historisches Dokument zum Stand 0.3.x. Für den zentralen Warenfluss, die mitgelieferten Baupläne und den Build gilt die README von 0.5.0-dev.

# LogisticColonies 0.3.0-dev — Kolonieübergreifende automatische Transporte

## Grundsatz

- Die Fracht folgt weiterhin den **physischen** Little-Logistics-Schiffs- und Bahnlinien.
- LogisticColonies **lädt/entlädt** Fahrzeuge an den konfigurierten Docking-Stations.
- Die Warenanforderungen werden **aus dem vorhandenen MineColonies-Request-System gelesen**, nicht als eigene MineColonies-Requests gefälscht.
- Nur offene `Stack`-Anfragen am **Player- oder Retrying-Resolver** werden im Export berücksichtigt. Requests, die gerade aktiv von normalen MineColonies-Craftern/Kurieren betreut werden, werden nicht abgefangen.
- MineColonies entscheidet nach dem Import unverändert selbst über die weitere Versorgung seiner Arbeiter. Der Import sollte daher in ein vom MineColonies-Lagersystem genutztes Inventar (z. B. angebundenes Rack) erfolgen.
- Die Aufträge und die Routen funktionieren in dieser Version **nur innerhalb derselben Dimension**. Zwischen verschiedenen Dimensionen existiert noch keine Transportvermittlung.

## Einrichtung

1. In Quellkolonie und Zielkolonie jeweils Hafen/Bahnhof + Logistikzentrum bauen, Dockarbeiter und Controller zuweisen. **Für den Export** muss das Quell-Logistikzentrum besetzt sein. Für den Import muss mindestens ein Dockarbeiter vor Ort beschäftigt sein.
2. Pro Gleis bzw. Schiffsliegeplatz einen realen Little-Logistics-Docking-Station-Block aufstellen, plus ein Lager mit NeoForge-ItemHandler.
3. Mit dem Structurize Tag Tool `gleis1` bzw. `schiffsdock1` und `lager1` markieren und per `/logisticcolonies tags sync <x> <y> <z>` erkennen lassen. Alternativ manuell `/logisticcolonies link <HUT> <Dock> <Lager>`.
4. In der **Quellkolonie** `/logisticcolonies mode <HUT> export` und im **Ziel** `/logisticcolonies mode <HUT> import` setzen.
5. Route pro Quell-Dock festlegen: `/logisticcolonies route berth <Quell-HUT> <Slot 1..5> <Ziel-HUT>` (alle Positionsangaben sind Minecraft-Blockkoordinaten, also 3 Zahlen je Position).
6. Little-Logistics-Fahrpläne selbst so konfigurieren, dass das Fahrzeug an genau diesem Quell-Dock zu dem angegebenen Ziel-Dock fährt. LogisticColonies kann die tatsächliche Fahrroute derzeit **nicht** verifizieren.
7. Ein offener MineColonies-Request am Player-/Retrying-Resolver der Zielkolonie veranlasst automatisch einen Export, wenn passende Items im Quell-Lager vorhanden sind, ein Dockarbeiter und Controller arbeiten und ein Fahrzeug tatsächlich angedockt ist.
8. Über `/logisticcolonies status <Quell-HUT>` die einzelnen Dock-Ziele kontrollieren und über `/logisticcolonies demands <Ziel-HUT>` die verwendbaren nativen Requests anzeigen.

## Weitere Befehle

| Befehl | Wirkung |
|---|---|
| `route <Quelle> <Ziel>` | Alte Syntax, setzt das **Standardziel** für alle Docks ohne eigene Route (nur gleicher Besitzer) |
| `route berth <Quelle> <Slot> <Ziel>` | Individuelles Ziel für genau einen Dockplatz (gleicher Besitzer) |
| `route foreign <Quelle> <Slot> <Ziel>` | Route **zwischen verschiedenen Besitzern** explizit freigeben, **OP-Stufe 4** erforderlich |
| `route remove <Quelle> <Slot>` | Individuelle Route entfernen, dann gilt ggf. das Standardziel |
| `route reset <Quelle>` | Alle Routen entfernen, ohne bereits verladenen Versandstand zu löschen |
| `status <HUT>` | Gebäudestufe, Belegungsstatus, Dock-Routen und Versandbuchungen |
| `demands <Ziel-HUT>` | Automatisch verwendbare MineColonies-Anforderungen und reservierte Mengen |

Für alle Befehle ist das Präfix `/logisticcolonies` erforderlich. Alle außer `route foreign` erfordern OP-Stufe 2.

## Sicherheits- und Mengenschutz

- Standardmäßig akzeptiert die Route **nur Kolonien desselben Besitzers**. Besitzerwechsel werden bei jedem Export erneut geprüft.
- Eine Route zu einer fremden Kolonie erfordert den **separaten** `route foreign`-Befehl mit OP-Stufe 4. Die Freigabe ist an die Besitzer-UUIDs zum Freigabezeitpunkt gebunden; nach Besitzerwechsel wird der Export bis zur erneuten Freigabe verweigert. Dies ist eine administrative Vertrauensentscheidung, keine automatisch erkennbare Zustimmung beider Spieler.
- Jede Versandbuchung wird als `Colony-ID | originaler MineColonies-Request-Token` gespeichert.
- Mehrere Exportgebäude teilen ein **globales Mengenbudget** je Dimension und Anfrage: Sind 96 Items angefordert und wurden 64 bereits verladen, dürfen andere Exporteure zusammen nur noch 32 verladen.
- Reservierungen verbleiben bei laufenden MineColonies-Requests, auch wenn diese zwischenzeitlich nicht mehr vom Player-Resolver betreut werden. Erst nachdem ein Request abgeschlossen, storniert oder aus dem Request-System entfernt wurde, werden die Buchungen entfernt.
- Versendete Items gelten **nicht** allein durch das Verladen als zugestellt. Es wird keine direkte Request-Abschließung vorgenommen.
- Bestehende Einzelziel-/Einzeldock-Verbindungen aus Version 0.2.x werden weiterhin aus `logisticcolonies_network_v1` gelesen. Alte unqualifizierte Versandschlüssel bleiben für die Überbuchungsprüfung konservativ berücksichtigt.
- Routen werden nicht automatisch zwischen den Dimensionen verbunden, und Lager außerhalb der zuständigen Quellkolonie werden nicht angefasst.

## Wichtige noch offene Punkte (kein fertiges Transportsystem)

1. **Frachtmanifest je Fahrzeug** mit echter Lieferbestätigung und Wiederanlauf nach Zerstörung/Verlust fehlt. Der aktuelle Versandzähler ist eine konservative Verladungsbuchung, keine bestätigte Ankunft.
2. **Nativer eigener MineColonies-Request-Resolver** fehlt weiterhin. Das System liest nativen Nachfragebestand am Player-/Retrying-Resolver und löst nach Entladung eine erneute Kolonieprüfung aus.
3. Ohne Einbindung der importierten Ware in die normale **MineColonies-Lagerverwaltung** erkennt deren eigener Kurier keinen neuen verfügbaren Lagerbestand. Ein beliebiges Fass reicht daher nur als Test-Buffer, nicht als endgültige Kolonieversorgung.
4. Keine verifizierte Little-Logistics-Fahrtroute, daher genau ein Ziel **pro Quell-Dock** und physische Route passend dazu einrichten.
5. Noch keine Cross-Dimension-Unterstützung, keine GUI, kein AE2-ME-Export und keine Create-Stock-Link-Bestellung.
6. Ohne Schematic-Baupläne und erfolgreichen NeoForge-Build **nicht veröffentlichungsreif**.
