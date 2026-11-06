# Entwicklungsabhängigkeiten

Für `./gradlew build` werden diese Original-JARs benötigt:

- `minecolonies-1.1.1403-1.21.1.jar`
- `littlelogistics-mc1.21.1-v1.21.1.1-beta.2.jar`
- `structurize-1.0.835-1.21.1-snapshot.jar`
- `blockui-1.0.210-1.21.1-snapshot.jar`
- `multipiston-1.2.58-1.21.1.jar`
- `domum-ornamentum-1.0.236-snapshot-main.jar`

Optionale Integrationen:

- `create-1.21.1-6.0.10.jar`
- `appliedenergistics2-19.2.18.jar`

Für Spielstarts auch deren transitive Laufzeitabhängigkeiten wie Ponder,
Flywheel und GuideME gemäß den jeweiligen Mod-Metadaten installieren.
Zusätzliche Laufzeitmods lassen sich im `mods`-Ordner des Entwicklungsstarts
ablegen; diese Dateien werden nicht in die Addon-JAR eingebettet.

Die JARs sind nicht mitgeliefert und werden von Git ignoriert. Beziehe sie aus
den offiziellen Projektveröffentlichungen. Die Dateinamen entsprechen dem
bereitgestellten Prototyp; andere Versionen sind nicht damit validiert.
`bash scripts/test-core.sh` benötigt diese Abhängigkeiten nicht.
