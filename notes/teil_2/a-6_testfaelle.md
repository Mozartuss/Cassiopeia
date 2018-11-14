# Aufgabe, Teil 2

## Testfälle

### A-6, a

Gegenüberstellung der Vor- und Nachteile einer möglichst frühen Auseinandersetzung mit der Test-Problematik.

*Pro*
 - andere Herangehensweise an das Problem die bei der Programmierung vorteilhaft sein kann
 - es entstehen alternative Sichtweisen auf das Problem
 - konkret festgelegte Tests können schon ein großer Teil der Problemlösung sein
 - konzentration auf das Wesentliche

*Contra*
 - Implementierungs-Details noch unbekannt -> Sinnvolle Tests nur bedingt möglich 
 - Spezifikationsänderungen machen frühere Überlegungen zunichte


### A-6, b

Mögliche Testfälle für das physikalische Modell:

- die Masse eines Körpers muss positiv sein
- die Masse eines Körpers darf nicht Null sein
- zwei Körper dürfen nicht den selben Ortsvektor besitzen
- Ortsvektoren müssen innerhalb des festgelegten Raumbereichs sein
- Zeitintervall (T-Delta) darf nicht Null sein


### A-6, c

Beziehung zwischen den Anforderungen aus A-1b und den Testfällen.

Parallelisierung:
 - sind sämtliche CPU-Kerne ausgelastet?

Architektur:
 - Rechenergebnis unabhängig von der Anzahl der eingesetzten CPUs
 - Grafik-Simulation beeinflusst nicht das Rechenergebnis bzw. die Schnelligkeit der Berechnung

GUI:
 - Eingabemaske für sämtliche Parameter

Parameter:
 - erforderliche Parameter auf Vorhandensein prüfen
 - Bereichsprüfung jedes einzelnen Parameters

Simulation:
 - startet erst wenn alle Parameter gegeben sind
 - Beenden der Simulation erfolgt unmittelbar


### A-6, d

Testfälle für das zu implementierende Gesamtsystem:

- läuft auf jedem Client die gleiche Python-Version
- sind alle Clients über das Netzwerk erreichbar
- sind die Latenzen im Netz so klein, dass sie die Berechnungszeit nicht beeinflussen
- sind die (Rechen-) Ergebnisse unabhängig von der Anzahl der eingesetzten Clients

