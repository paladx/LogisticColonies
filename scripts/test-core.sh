#!/usr/bin/env bash
# Java-21-only core tests, no Minecraft/NeoForge downloads required.
set -euo pipefail
cd "$(dirname "$0")/.."
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
S=src/main/java/de/logisticcolonies/logistics
T=src/test/java/de/logisticcolonies/logistics
if command -v javac >/dev/null 2>&1; then
  compiler=(javac)
else
  # Some cloud images include the JDK compiler module but omit its launcher.
  compiler=(java -m jdk.compiler/com.sun.tools.javac.Main)
fi
"${compiler[@]}" -source 21 -target 21 -encoding UTF-8 -d "$TMP" \
  "$S/BuildingTiers.java" "$S/BerthScheduler.java" "$S/LogisticsTagNames.java" \
  "src/main/java/de/logisticcolonies/traffic/TrafficArbiter.java" "$S/ShipmentAccounting.java" "$S/RouteSecurity.java" "$S/DetachedReservations.java" \
  "$T/BuildingTiersTest.java" "$T/BerthSchedulerTest.java" "$T/LogisticsTagNamesTest.java" \
  "$T/TrafficArbiterTest.java" "$T/ShipmentAccountingTest.java" "$T/RouteSecurityTest.java" "$T/DetachedReservationsTest.java"
for name in BuildingTiers BerthScheduler LogisticsTagNames ShipmentAccounting RouteSecurity DetachedReservations TrafficArbiter; do
  java -ea -cp "$TMP" "de.logisticcolonies.logistics.${name}Test"
done
