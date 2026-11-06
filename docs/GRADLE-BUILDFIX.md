> Historisches Dokument zum Stand 0.3.x. Für den zentralen Warenfluss, die mitgelieferten Baupläne und den Build gilt die README von 0.5.0-dev.

# Gradle-Konfigurationsfehler — Lösung 0.2.1-dev

**Fehler:** `Could not set unknown property 'logLevel' for object of type net.neoforged.gradle.common.runs.run.RunImpl.`

**Grund:** `logLevel` ist in dieser NeoGradle-Run-Konfiguration keine unterstützte Property.

**Korrektur in `build.gradle`:**

```groovy
runs {
    configureEach {
        systemProperty 'forge.logging.markers', 'REGISTRIES'
        systemProperty 'forge.logging.console.level', 'info'
    }
    client { }
    server { }
}
```

**So erneut testen:** Gradle-Projekt neu laden, vorhandene Mod-JARs nach `libs/` kopieren, dann `gradle build --stacktrace`.
Ein erfolgreiches Compile wurde für 0.2.1-dev hier nicht nachgewiesen.
Weitere Fehler bitte als neues Log bereitstellen.
