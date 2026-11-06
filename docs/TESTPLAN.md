> Historisches Dokument zum Stand 0.3.x. Für den zentralen Warenfluss, die mitgelieferten Baupläne und den Build gilt die README von 0.5.0-dev.

# Testplan — LogisticColonies 0.2.2-dev

In einer **neuen Testwelt** auf NeoForge 1.21.1 mit den exakt genannten Mods testen.

1. Build: `gradle build` kompiliert ohne Fehler; JAR in frischen Modpack-Server legen.
2. Dedizierter Server und Client starten, alle 3 Hut-Blöcke vorhanden, keine Registry-/Sound-Fehler.
3. Jede Hütte einem Koloniegebäude zuweisen, Dockarbeiter (Hafen/Bahnhof) bzw. Controller (Logistikzentrum) anstellen.
4. Hafen-Docking-Station mit Boot+Barge verbinden. Bahn-Docking-Station mit Güterwaggon verbinden.
5. `link` für Lager-Rack und Dock ausführen, `mode import`, Fahrzeuge mit Ladung anlegen: Lieferung geht ins Rack.
6. Quelle `mode export`, Ziel `mode import`; `route` setzen; Little-Logistics-Fahrroute einrichten.
7. Offener MineColonies-Request fällt auf Spielerresolver zurück: passenden Warenbestand in Quell-Rack legen;
   Controller und Dockarbeiter besetzen; Versand wird nur einmal reserviert und mit Schiff/Zug transportiert.
8. Wenn Ziel-Rack Bestand erhält, soll die MineColonies-Request-Neuprüfung ausgelöst werden.
9. Save/reload, `status` prüfen: Positionen, Modus, Ziel und Reservierungen bleiben erhalten.
10. Offlineziel, voller Lagerbestand, leere Docking-Station, abgebrochener Request, Item mit DataComponents,
    64+ Items, 2 unterschiedliche Anfragen, Wechsel des Fahrzeugs und Chunk-Unload testen.
11. Speicher an einem AE2-Interface oder Create-ItemHandler testen, sofern diese Komponenten einen
    NeoForge-Block-ItemHandler exponieren; ME-Autocrafting/Stock Links sind noch NICHT implementiert.
12. Test auf verlorene Fracht, Doppelversand, Inaktivität und Chunk-Grenzen durchführen.

**Bekannte Einschränkung:** Es fehlen aktuell MineColonies-Blueprints. Die reguläre
Gebäudeplatzierung/-entwicklung über das Build Tool ist ohne zusätzliche Strukturen nicht komplett.


## Regressionen für Mehrfach-Docks und Stufen 1–5

13. **Aufstieg:** Pro Gebäudestufe jeweils ein neues physisches Little-Logistics-Dock bauen und mit
    `link` registrieren. Maximal zulässige Dockzahl muss 1, 2, 3, 4, 5 entsprechen. Der
    Versuch, mehr Docks einzutragen, muss mit Fehlermeldung abgewiesen werden.
14. **Gleichzeitigkeit:** An mindestens drei Docks eines Stufe-3-Hafens unterschiedliche
    Schiffe mit unterschiedlichen Waren andocken lassen. Mit drei Arbeitern müssen alle drei
    innerhalb desselben 20-Tick-Zyklus entladen; mit nur zwei Arbeitern darf nur zwei der ersten
    zwei Docks aktiv sein. Den gleichen Test für einen Bahnhof mit drei Zügen ausführen.
15. **Ohne Fahrzeug:** Ein konfiguriertes, aber leeres Dock muss unverändert bleiben. Die
    Verarbeitung darf nicht Items in ein Phantom-Inventar laden.
16. **Herabstufung:** Stufe 5 mit fünf Docks zurück auf 2 setzen. Nur die ersten beiden
    verknüpften Docks werden bedient; die übrigen bleiben in den SavedData-Einträgen erhalten.
17. **Weiteres Dock:** Ein zweites `link` mit demselben Dock und anderem Lager aktualisiert
    ausschließlich dieses Dock. Ein Dock darf nicht parallel von zwei Gebäuden verwaltet werden.
18. **Persistenz/Migration:** Bestehende v1-SavedData mit genau einem Dock laden. Ein zweites Dock
    verknüpfen, Welt speichern, Server neu starten: Reihenfolge und Lagerpaare müssen erhalten sein.
19. **RS-Parallelität:** Mehrere Docks dürfen nicht den gleichen Anfrage-Token mehrfach über
    die geforderte Gesamtmenge hinaus bedienen. Besonders 2×64 Items bei nur 96 angefordert testen.
20. **Betriebsrichtungen:** `mode import/export` muss für alle Docks des Gebäudes gelten;
    korrektes Importlager je Dock und keine unmittelbare Rückladung verifizieren.
21. **Controller-Stufen:** Beim Logistikzentrum müssen 1/2/2/3/3 Controllerstellen möglich sein.
22. **Baupläne:** Vor Freigabe als spielbare Version müssen die 15 Structurize-Schematics für
    Hafen/Bahnhof/Logistikzentrum (je 5) erstellt und Build-Tool-Upgrades getestet werden.

## Ohne Minecraft ausführbare Tests

Die reine Java-Kapazitätslogik kann unabhängig von NeoForge geprüft werden:

```bash
mkdir -p /tmp/lc-tier-tests
javac -encoding UTF-8 -d /tmp/lc-tier-tests \
  src/main/java/de/logisticcolonies/logistics/{BuildingTiers,BerthScheduler}.java \
  src/test/java/de/logisticcolonies/logistics/{BuildingTiersTest,BerthSchedulerTest}.java
java -ea -cp /tmp/lc-tier-tests de.logisticcolonies.logistics.BuildingTiersTest
java -ea -cp /tmp/lc-tier-tests de.logisticcolonies.logistics.BerthSchedulerTest
```

Die Tests decken Kapazitäten, Beschäftigungsgrenzen, Stufen-Rückbau, Rundlauf-Fairness und
Berücksichtigung angedockter Fahrzeuge ab. Sie ersetzen keinen vollständigen Mod-Build.

## Gradle-Tests im Projekt 0.2.2-dev

`BuildingTiersTest` und `BerthSchedulerTest` haben jeweils eine `main()`-Methode,
keine JUnit-`@Test`-Methoden. Der frühere Gradle-Testlauf schlug deshalb mit
`no tests discovered` fehl. Die zwei Tests werden nun mit JavaExec und aktivierten
Java-Assertions (`-ea`) ausgeführt. `gradle test` und `gradle build` führen sie automatisch aus.
`failOnNoDiscoveredTests = false` verhindert nur den falschen Fehler des JUnit-Discovery-Schritts;
die beiden eigentlichen Prüfprogramme bleiben Bestandteil des Builds.

## 0.3.0-dev: Automatische Kolonierouten

23. Mindestens zwei Kolonien **desselben Besitzers** und pro Kolonie einen Hafen/Bahnhof anlegen. Ein Quelldock mit `/logisticcolonies route berth <Quelle> 1 <Ziel>` konfigurieren. Bei gültigem Ziel-Request sollen passende Items nur auf das dem Ziel zugewiesene Fahrzeug verladen werden.
24. Ein Stufe-2-Quellbahnhof erhält zwei Dockplätze; Dock 1 fährt zu Kolonie B, Dock 2 zu Kolonie C (separate Import-Hütten). Zwei unterschiedliche Items bestellen. Beide Docks müssen ihre jeweilige Bestellung bedienen, niemals kreuzweise.
25. Zwei Quellkolonien beliefern dieselbe Zielanfrage (96 Items). Quellkolonie A lädt 64; Quellkolonie B darf höchstens 32 laden. Mit `demands <Ziel>` verifizieren.
26. Verschiedene Koloniebesitzer: Normale `route berth` wird abgewiesen. `route foreign` funktioniert nur mit OP-Level 4. Nach Rücknahme oder Besitzerwechsel erneuten Autorisierungscheck testen.
27. Anfrage bereits an normalen MineColonies-Kurier gebunden: LogisticColonies darf **keine** zusätzliche Exportladung erstellen. Bei Player-/Retrying-Resolver darf geladen werden.
28. Bei Import in ein **MineColonies-Lager-Rack** wird eine Bestandsaktualisierung ausgelöst. Anschließend muss die normale MineColonies-Versorgung den Request erfüllen; niemals Request direkt im Add-on als erfüllt markieren.
29. Nach Welt-Neustart müssen per-Dock-Routen, Cross-Owner-Freigaben und Reservierungen bestehen bleiben. Alte 0.2.4-Welten mit Standardroute müssen weiter funktionieren.
30. Transporte in andere Dimensionen müssen abgewiesen bzw. nicht ausgeführt werden. Bei fehlender oder falscher LL-Fahrroute darf keine erfolgreiche Lieferung behauptet werden.

**Ohne Mod-Downloads:** `bash scripts/test-core.sh` führt fünf reine Java-Prüfprogramme aus.
