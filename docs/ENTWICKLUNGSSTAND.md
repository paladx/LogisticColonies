# Entwicklungsstand 0.5.0-dev

Dieser Stand ergänzt 0.4.0-dev um den Tankwart, Schiffs- und Zugtankstellen sowie
Controller-Verkehrsabschnitte. Implementierung und Grenzen stehen in
`TANKSTELLEN-UND-VERKEHR.md`, der aktuelle Prüfnachweis in `PRUEFPROTOKOLL.md`.

Es gibt fünf HUT-Blöcke, drei Jobs und 25 eigene Structurize-Baupläne. Die bisherigen
Frachtfunktionen und die gespeicherten Logistiknetzwerke bleiben erhalten.
Verkehrsdefinitionen und Reservierungen besitzen eine zusätzliche SavedData-Datei.

Die neue Tankstellenfunktion nutzt die nativen Dampfmotor-Brennstoffhandler.
Die Verkehrskoordination verwendet vollständig erfasste Fahrzeugverbände,
persistente Bereichsreservierungen und eine temporäre Sperre vor dem Entity-Tick.
Sie verändert keine EngineOn-/Frozen-Flags und ersetzt die LL-Navigation nicht.

Zusätzlich wurde die Befehlsauflösung für das Logistikzentrum korrigiert: Der
Gebäude-Lookup akzeptiert nun auch das Zentrum; jeder Frachtbefehl prüft seinen
eigenen Gebäudetyp. Damit funktioniert auch die manuelle Hub-Zuordnung.

Nicht implementiert bleiben unter anderem Elektro-Ladung, globale Fahrplanauswahl,
Deadlock-Auflösung, Paket-Lieferquittungen, native Create-/AE2-Bestelladapter und
sichtbarer NPC-Warentransport. Der Kollisionsschutz gilt für konfigurierte Bereiche.
