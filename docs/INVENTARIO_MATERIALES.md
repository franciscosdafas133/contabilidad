# Inventario de materiales — Fundamentos de Contabilidad (UP 2026-2)

**Fuente raíz:** `OneDrive_2026-09-11/Fundamentos de Contabilidad`  
**Criterio:** cada fila describe qué aporta el archivo al motor educativo determinístico.  
**Leyenda de prioridad:** crítica = regla/test del MVP · importante = estructura pedagógica · complementaria = contexto o duplicado.

**Convención de estados (nomenclatura del curso):**
- **ESF** — Estado de Situación Financiera (también “Balance General”)
- **ER** — Estado de Resultados (en Presentación 3 también “Estado de Resultados Integrales” / “Ganancias y Pérdidas”)
- **ECPN / ECPTN** — Estado de Cambios en el Patrimonio Neto
- **EFE** — Estado de Flujo de Efectivo

**Tipos de evidencia en “Conocimiento aportado”:**
- `[R]` respaldado explícitamente por el archivo
- `[I]` inferido al cruzar con otros materiales (no usar solo como regla)
- `[P]` propuesta de diseño para el sistema (no es regla del curso)

---

## Resumen ejecutivo del corpus

| Grupo | Archivos | Rol para el motor |
|-------|----------|-------------------|
| Sílabo y cronograma | 2 | Secuencia pedagógica, unidades, evaluaciones |
| Semana 1 | 10 | Introducción, ecuación contable, ESF básico |
| Semana 2 | 9 | ESF avanzado (transacciones → ESF + IR/reserva) |
| Semana 3 y 4 | 11 | ER, ECPN, EFE, integración 4 EEFF |
| PDs 1–4 | 14 | Evaluaciones formativas + solucionarios golden |
| PCS (PC1) | 2 | Evaluación sumativa ESF (test crítico) |
| Notas | 1 | Administrativo; baja utilidad al motor |
| **Total** | **~49** | |

**Cobertura vs sílabo:** Unidades 1–4 bien respaldadas. Unidades 5–8 (diario/mayor, ajustes, ratios, costos/CVU, PCGA avanzado) **sin materiales de práctica** en esta carpeta.

---

## Tabla maestra

| Archivo | Tipo | Tema | Estado(s) | Conocimiento aportado | Uso futuro | Prioridad |
|---------|------|------|-----------|------------------------|------------|-----------|
| `Sílabo y cronograma/Fundamentos de Contabilidad - 160092 - P (2026-02-PRE).pdf` | teoría / sílabo | Unidades 1–8, logros, evaluación | ESF, ER, ECPN, EFE (+ciclo, ratios, costos) | `[R]` nombres oficiales de estados; logros por unidad; PCGA; ciclo contable posterior; bibliografía Warren/Horngren | Definir alcance MVP = U1–4; glosario oficial | crítica |
| `Sílabo y cronograma/FC 26-2 CRONOGRAMA ALUMNOS v08.08.26 (1).xlsx` | plantilla / cronograma | Semanas 1–16, PD/PC | todos EEFF | `[R]` orden real: clasificación→ESF→ER/ECPN→EFE+integración→diario→ajustes; PD1–9 y PC1–5 temas; EFE “directo e indirecto” con énfasis temprano en directo | `MODELO_PEDAGOGICO_ACTUAL`; roadmap de modos UI | crítica |
| `Notas Fundamentos de Contabilidad_Pre.xlsx` | otro | notas | — | Administrativo | Ignorar en motor | complementaria |

### Semana 1

| Archivo | Tipo | Tema | Estado(s) | Conocimiento aportado | Uso futuro | Prioridad |
|---------|------|------|-----------|------------------------|------------|-----------|
| `Presentación 1 Introduccion...ppt` | diapositivas | Qué es contabilidad, usuarios, ecuación, partida doble, EEFF | intro | `[R]` *(texto extraído)* ecuación A=P+PN; partida doble (≥2 cuentas); lista de 4 EEFF; ciclo registro→clasificación→análisis→resumen; usuarios internos/externos; financiera vs administrativa | Nivel 1 conceptual; validación partida doble | importante |
| `Presentación 2 Estado Situación Financiera...ppt` | diapositivas | Definiciones ESF, catálogo de cuentas, encabezado | ESF | `[R]` *(texto extraído)* AC (disponible/exigible/realizable), ANC (tangible/intangible/LP), PC/PNC, PN; contra-activos; sobregiro antes de tributos; partidas diferidas CP/LP; plantilla de presentación; **nota:** anticipo de clientes aparece como “activo negativo” (tensión vs PDs/PC → ver D17) | Catálogo de cuentas; plantilla ESF; orden de exposición | crítica |
| `2. FC Cuentas del Estado de Situación Financiera.pdf` | teoría | Definiciones de cuentas ESF | ESF | `[R]` significado de cada cuenta (efectivo, CxC, mercadería, intangibles, pasivos, anticipos, etc.) | Textos de ayuda / feedback de clasificación | crítica |
| `Análisis adicional de algunas cuentas del ESF (9).pptx` | diapositivas | Cuentas especiales + cálculos | ESF (+efecto en resultados) | `[R]` estimación cobranza dudosa; entregas a rendir; existencias por recibir; depreciación (costo−rescate)/vida; amortización sin rescate; gastos/ingresos adelantados; anticipos; **reserva legal 10% UN con tope 20% capital** | Reglas de cálculo ESF/cierres; tests unitarios | crítica |
| `Ejercicio 1 (Ecuacion contable) (2).docx` | ejercicio | Ecuación contable | ecuación → EEFF | `[R]` operaciones simples que afectan A/P/PN | Fixture de entrada Nivel 2 | importante |
| `Solejercicio1_EEFF (1) (8).xlsx` | solución | Solución Ej.1 | ecuación / EEFF | `[R]` saldos esperados por pregunta | Test golden | crítica |
| `Ejercicio 2 Ecuación contable (3).doc` | ejercicio | Casos A/B ecuación | ecuación | `[R]` narrativa de transacciones + costo de ventas | Input tests | importante |
| `solucionario ejercicio 2 ecuación contable (3).xlsx` | solución | Matriz ecuación casos 1–2 | ecuación | `[R]` columnas de cuentas; filas por operación; totales; doble efecto venta/CV | **Fixture canónico de ecuación contable** | crítica |
| `Ejercicio 3(ESF) (6).docx` | ejercicio | Armar ESF con orden correcto | ESF | `[R]` énfasis en presentación/orden de cuentas | Modo A ESF | importante |
| `solejercicio3 ESF (1) (2).xlsx` | solución | ESF Ej.3 | ESF | `[R]` estructura y saldos correctos | Test golden ESF | crítica |

### Semana 2

| Archivo | Tipo | Tema | Estado(s) | Conocimiento aportado | Uso futuro | Prioridad |
|---------|------|------|-----------|------------------------|------------|-----------|
| `Análisis adicional...pptx` (duplicado S1) | diapositivas | Igual que S1 | ESF | Duplicado exacto | No duplicar reglas | complementaria |
| `Ejercicio ESF Empresa Super Smash (2).doc` | ejercicio | Transacciones → ESF | ESF | `[R]` caso comercial con múltiples operaciones | Input PD-like | importante |
| `solejercicio 4 ESF Super Smash.xlsx` | solución | Ecuación + impuesto + ESF | ESF | `[R]` flujo: matriz→UAIR→IR 29.5%→UN→reserva→ESF equilibrado | Test integración ecuación→ESF | crítica |
| `Ejercicio 5 ESF.docx` | ejercicio | Pearson & Specter | ESF | `[R]` transporte en compra; devoluciones; anticipos; préstamos CP/LP; intangibles; IR/reserva | Casos edge; reglas condicionales | crítica |
| `solejercicio 5.xlsx` | solución | Ecuación + ESF | ESF | `[R]` saldos y presentación | Test golden | crítica |
| `Ejercicio 6.doc` | ejercicio | Villamar Fish (saldos + hechos) | ESF (+efectivo, RA) | `[R]` saldos iniciales + transacciones; hojas auxiliares efectivo/RA | Input complejo ESF | importante |
| `solejercicio 6.xlsx` | solución | ESF + efectivo + u retenidas | ESF | `[R]` conciliaciones parciales; IR sobre UAIR; reserva | Test golden avanzado | crítica |
| `Ejercicio 7 ESF (1).doc` | ejercicio | ESF | ESF | `[R]` práctica adicional | Banco de ejercicios | complementaria |
| `solejercicio 7.xlsx` | solución | ESF | ESF | `[R]` saldos | Test | importante |

### Semana 3 y 4

| Archivo | Tipo | Tema | Estado(s) | Conocimiento aportado | Uso futuro | Prioridad |
|---------|------|------|-----------|------------------------|------------|-----------|
| `Presentación 3 Estado de Resultados y ECPN.ppt` | diapositivas | ER + ECPN | ER, ECPN | `[R]` *(texto extraído)* también llamado “Estado de Resultados Integrales”; ER por período (no acumulativo); CV = II+CN−IF; CN = compras+incidentales−dev/reb; **sistema periódico** (*usado en el curso*); estructura ECPN | Plantillas ER/ECPN; flag sistema periódico | crítica |
| `Presentación 4 Estado de Flujo de Efectivo (5).ppt` | diapositivas | EFE | EFE | `[R]` *(texto extraído)* efectivo = caja+bancos+inv. CP; fuente/uso; AO/AI/AF con ejemplos; métodos directo e indirecto (ambos nombrados) | Clasificación EFE; plantilla; no implementar indirecto sin golden | crítica |
| `Detalle de algunas cuentas del Estado de Resultados...(9).pptx` | diapositivas | Cuentas ER + vínculo ESF | ER, ESF | `[R]` dscto pronto pago otorgado (resta ventas); recibido (afecta CV); devoluciones/rebajas; donaciones; pérdida mercadería; **antes/después dual ESF+ER** | Reglas ER; demos de efecto cruzado | crítica |
| `Ejemplo de Estado de Resultados.xlsx` | plantilla / ejemplo | ER PODER SAC | ER | `[R]` estructura: ventas→UB→partidas operativas→UO→partidas financieras→UAIR→IR→UN | Plantilla canónica ER + test | crítica |
| `1. Ejercicio sobre ER ECPN EFE Cia Las Vegas.docx` | ejercicio | ER+EFE; ECPN+clasificación AF | ER, EFE, ECPN | `[R]` datos narrativos multiestado; preguntas de clasificación AF | Input integración parcial | crítica |
| `1. solucionario...Las Vegas...(1).xlsx` | solución | ER + EFE + ECPN Valparaíso | ER, EFE, ECPN | `[R]` CV con robo; alquiler prorrateado; EFE directo; ECPN con reinversión/reservas; AF = aportes y dividendos | Tests golden multiestado | crítica |
| `2. Ejercicio sobre ER.doc` | ejercicio | ER | ER | `[R]` práctica ER | Input | importante |
| `2. Solución del Ejercicio sobre ER.xlsx` | solución | ER | ER | `[R]` saldos | Test | importante |
| `Ejercicio (4 Estados financieros) Cia Chicago.xlsx` | ejercicio | 4 EEFF (enunciado denso) | ESF, ER, ECPN, EFE | `[R]` saldos iniciales/finales parciales + hechos; CV auxiliar | Práctica; **no golden completo** (sin solucionario cerrado) | importante |
| `Ejercicio (4 Estados Financieros) Cia Park City (3).xlsx` | ejercicio | Pedir 4 EEFF | 4 EEFF | `[R]` saldos 31-12-19 + 13 hechos | Input golden integración | crítica |
| `solucionario...Park City (2).xlsx` | solución | 4 EEFF + hoja de trabajo | 4 EEFF | `[R]` ER/ECPN/EFE/ESF interrelacionados; CV; prorrateos; **ojo: zona con `#REF!`** | Test integración principal; marcar inconsistencia | crítica |

### PDs

| Archivo | Tipo | Tema | Estado(s) | Conocimiento aportado | Uso futuro | Prioridad |
|---------|------|------|-----------|------------------------|------------|-----------|
| `PDs/PD1/...Enunciado.docx/.pdf` | evaluación | Clasificación + ecuación BikeAndes | clasificación, ecuación | `[R]` taxonomía Activo/Pasivo/PN/Ingreso/Gasto; 15 transacciones | Nivel 1–2; fixtures | crítica |
| `PDs/PD1/...Solucionario.xlsx` | solución | Ej.1–2 | clasificación, ecuación | `[R]` respuestas correctas | Tests golden PD1 | crítica |
| `PDs/PD2/...Enunciado.docx` + `PD2.pdf` | evaluación | Depreciación; ESF desde transacciones; armado ESF por saldos; PCGA/partida doble | ESF | `[R]` fórmulas dep. con tasa/rescate; ESF mensual; lista desordenada→ESF | Tests PD2; reglas depreciación | crítica |
| `PDs/PD2/...Solucionario.xlsx` | solución | E1–E4 | ESF | `[R]` saldos y ESF | Golden | crítica |
| `PDs/PD2/Chuleta_PD2_Contabilidad IA.docx` | otro / guía JP | Timing de clase | — | `[I]` método Socrático del JP (no reglas contables nuevas) | Diseño UX de hints, no motor | complementaria |
| `PDs/PD2/Metodologia_PD2_Contabilidad IA.docx` | otro / guía JP | Cómo enseñar PD2 | — | `[R]` patrón: qué pide / qué falta → intento → regla → número | Feedback pedagógico | importante |
| `PDs/PD3/...Documento.docx/.pdf` | evaluación | ER; ECPN; EFE aislados | ER, ECPN, EFE | `[R]` construcción por estado con datos tabulares | Modo A multiestado | crítica |
| `PDs/PD3/...Solucionario.xlsx` | solución | E1 ER / E2 ECPTN / E3 EFE | ER, ECPN, EFE | `[R]` plantillas completas; tope reserva legal; EFE directo AO/AI/AF | Golden PD3 | crítica |
| `PDs/PD4/...Enunciadovf.docx/.pdf` | evaluación | EFE; integración Sapiense (completar 4) | EFE, 4 EEFF | `[R]` no monetarias (aporte en equipos); dividendos declarados no pagados fuera de EFE; hallar efectivo de venta de terreno | Golden integración | crítica |
| `PDs/PD4/...Soluciónvf.xlsx` | solución | EFE Terracan; Sapiense completo | EFE, ESF, ER, ECPN | `[R]` nota explícita aportes no monetarios; reconciliación ESF | Test más cercano a PC2 | crítica |

### PCS

| Archivo | Tipo | Tema | Estado(s) | Conocimiento aportado | Uso futuro | Prioridad |
|---------|------|------|-----------|------------------------|------------|-----------|
| `PCS/FC PC1 2026-2 Enunciado.pdf` | evaluación | Completar ESF; ESF desde saldos+transacciones | ESF | `[R]` estilo examen; IR 29.5%; reserva 10%; depreciaciones prorrateadas; “movimientos de efectivo ya incorporados” | Diseño Modo E; no filtrar enunciados a alumnos si se usa como banco secreto | crítica |
| `PCS/FC PC1 2026-2 Solucionario.xlsx` | solución | Sol_P1 ESF; Sol_P2 matriz+ESF | ESF | `[R]` ESF con puntaje por celda; matriz de ecuación tipo PC | **Test de aceptación duro del motor ESF** | crítica |

---

## Qué aporta cada archivo al motor (síntesis por capa)

### Capa conocimiento (catálogo / reglas)

- Presentación 2 + PDF cuentas ESF + PPTX análisis ESF → **catálogo y semántica de cuentas**.
- Presentación 3 + Ejemplo ER + PPTX detalle ER → **estructura ER y CV periódico**.
- Presentación 3/4 + PD3/PD4 → **ECPN y EFE (directo)**.
- PPTX reserva legal + solucionarios → **IR 29.5%, RL 10%, tope 20% capital**.

### Capa motor (transición de estado)

- Solucionarios de ecuación (Ej.2, Super Smash, PC1 P2, PD1) → modelo `filas de transacción → saldos`.
- PD2 E1 → motor de **depreciación/amortización**.
- Cierres en ESF (PC1, Ej.5–6) → pipeline UAIR→IR→UN→RL→RA.

### Capa EEFF / integración

- PD3 = estados aislados.
- Las Vegas / Park City / PD4 Sapiense = **cadena entre estados**.
- PPTX detalle ER = evidencia de UI “antes/después dual” ESF+ER (no necesariamente 4 paneles).

### Capa tests

Prioridad de fixtures golden (ver también `PLAN_IMPLEMENTACION.md`):

1. Ecuación Semana 1 caso 1–2  
2. Super Smash / Ej.5 / Ej.6  
3. PC1 Sol_P1 y Sol_P2  
4. PD1–PD4 solucionarios  
5. Las Vegas + Valparaíso  
6. Park City (con triage de `#REF!`)  
7. Ejemplo ER PODER SAC  

---

## Clasificación de tipo de material (conteo aproximado)

| Tipo | Cantidad aprox. |
|------|-----------------|
| Teoría / sílabo | 3 |
| Diapositivas | 7 (4 ppt + 3 pptx; 1 pptx duplicado) |
| Ejercicio / enunciado | ~18 |
| Solución / solucionario | ~16 |
| Evaluación (PD/PC) | 6 paquetes |
| Plantilla / ejemplo | 2 |
| Guía JP / otro | 3 |

---

## Vacíos detectados

| Vacío | Evidencia | Implicación |
|-------|-----------|-------------|
| Sin PD5–PD9 ni PC2–PC5 en carpeta | Solo PD1–4, PC1 | MVP no debe prometer diario/mayor/ajustes/ratios/costos |
| Chicago sin solucionario cerrado | Solo enunciado xlsx | Usar como práctica, no como assert estricto |
| Park City `#REF!` | Solucionario | Investigar antes de forzar reglas |
| Presentaciones .ppt extraídas en análisis | Texto incorporado a este inventario y a D16 | No usar dumps como runtime; fuente = .ppt originales |

---

## Separación respaldado / inferido / propuesto

| Afirmación | Clase | Fuente |
|------------|-------|--------|
| Los 4 EEFF se llaman ESF, ER, ECPN, EFE | respaldado | Sílabo, Presentación 1 |
| El curso usa ecuación contable antes del diario | respaldado | Semana 1–2, PD1, cronograma (diario en Semana 6) |
| Reserva legal 10% UN con tope 20% capital | respaldado | PPTX análisis ESF |
| IR tercera categoría 29.5% | respaldado | PD3, PC1, múltiples ejercicios |
| Sistema de mercadería = periódico | respaldado | Presentación 3 |
| EFE temprano = método directo | respaldado en ejercicios; cronograma también menciona indirecto | PD3/PD4/Las Vegas/Park City |
| El ledger interno del MVP debe ser ecuación, no diario | **propuesto (diseño)** | Inferido de secuencia del curso |
| Vista 2×2 de 4 EEFF desde día 1 | **rechazado como MVP** | Cronograma enseña aislado primero |
