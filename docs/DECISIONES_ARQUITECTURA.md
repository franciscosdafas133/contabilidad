# DECISIONES DE ARQUITECTURA

Documento vivo de decisiones. Cada bloque usa el formato obligatorio.

Leyenda de evidencia: `[R]` respaldado por materiales · `[I]` inferido · `[P]` propuesta de diseño.

---

## D01 — Alcance del MVP = Unidades 1–4 (cuatro EEFF + ecuación)

**DECISIÓN:**  
El MVP cubre únicamente Introducción/ecuación, ESF, ER, ECPN, EFE e integración básica. Diario/mayor, ajustes, ratios y costos quedan fuera hasta existir materiales o una formalización aparte.

**EVIDENCIA:**  
`[R]` La carpeta de materiales solo contiene Semanas 1–4, PD1–PD4 y PC1. El sílabo define 8 unidades, pero no hay solucionarios de U5–U8 en el corpus.  
`[R]` Cronograma: PD1–PD4 y PC1/PC2 cubren EEFF; PD5+ abre ciclo contable.

**ALTERNATIVAS:**  
1) Planificar las 8 unidades desde el día 1.  
2) MVP solo ESF.  
3) MVP U1–4 (elegida).

**POR QUÉ:**  
Sin solucionarios no se pueden crear tests golden ni reglas verificables para diario/mayor. Ampliar alcance rompería el principio “nada importante entra solo por conocimiento general”.

**CONFIANZA:** Alta  

**FUENTE:**  
`Sílabo ... 160092 ...pdf`; `FC 26-2 CRONOGRAMA ...xlsx`; estructura de carpetas `Semana 1|2|3 y 4`, `PDs`, `PCS`.

---

## D02 — Fidelidad alta al curso UP, con parámetros configurables

**DECISIÓN:**  
Nomenclatura, plantillas y reglas siguen los solucionarios UP (p.ej. IR 29.5%, reserva legal 10% con tope 20% del capital). Tasas y parámetros viven en configuración, no hardcode disperso.

**EVIDENCIA:**  
`[R]` IR 29.5% aparece en PC1, PD3, Ej.5, Las Vegas, Park City.  
`[R]` Reserva legal 10% y tope 20% capital en PPTX “Análisis adicional… ESF”.  
`[R]` Nombres ESF/ER/ECPN/EFE en sílabo y Presentación 1.

**ALTERNATIVAS:**  
1) Herramienta genérica internacional.  
2) Copia literal hardcodeada sin config.  
3) Alta fidelidad + config (elegida).

**POR QUÉ:**  
El valor educativo es aprobar/entender **este** curso. Configurar tasas permite reutilizar el motor sin traicionar los golden tests del ciclo.

**CONFIANZA:** Alta  

**FUENTE:**  
Sílabo; PPTX análisis ESF; PC1; PD3; solucionarios Semana 2–4.

---

## D03 — Runtime sin LLM; motor determinístico

**DECISIÓN:**  
Prohibido usar LLM para calcular, clasificar o “decidir” resultados en ejecución. El LLM solo puede usarse en desarrollo (análisis/docs/código).

**EVIDENCIA:**  
`[P]` Requisito explícito del proyecto.  
`[R]` Los solucionarios son determinísticos (Excel con valores fijos).

**ALTERNATIVAS:**  
1) Tutor LLM que resuelve.  
2) Híbrido LLM+reglas.  
3) Solo reglas (elegida).

**POR QUÉ:**  
Misma entrada debe dar misma salida; las explicaciones deben citar `rule_id`, no prosa improvisada.

**CONFIANZA:** Alta  

**FUENTE:**  
Requisitos del proyecto; solucionarios xlsx.

---

## D04 — Ledger temprano = ecuación contable (no libro diario)

**DECISIÓN:**  
El estado interno del MVP es un vector/mapa de saldos de cuentas actualizado por transacciones tipadas al estilo de la **ecuación contable**. El libro diario se pospone a Fase 10.

**EVIDENCIA:**  
`[R]` Ejercicios Semana 1–2 y PD1 piden “registrar con ecuación contable”.  
`[R]` PC1 Sol_P2 usa matriz de cuentas × fechas.  
`[R]` Cronograma sitúa diario/mayor en Semana 6 (PD5), después de EEFF.

**ALTERNATIVAS:**  
1) Partir de asientos debe/haber.  
2) Partir de ecuación (elegida).  
3) Doble modelo desde el inicio.

**POR QUÉ:**  
Modelar diario primero desconectaría la app de cómo se evalúa PC1/PD1–2 y añadiría complejidad sin materiales de soporte en el corpus actual.

**CONFIANZA:** Alta  

**FUENTE:**  
`solucionario ejercicio 2...xlsx`; `FC 2026-2 PD 1`; `FC PC1 ... Solucionario.xlsx`; Cronograma.

---

## D05 — EEFF como proyecciones, no cuatro mundos editables

**DECISIÓN:**  
ESF, ER, ECPN y EFE son **vistas/proyecciones** sobre saldos + movimientos. El alumno no edita totales de un estado como fuente de verdad.

**EVIDENCIA:**  
`[R]` Park City / PD4 construyen los cuatro a partir de los mismos hechos.  
`[R]` Utilidad neta fluye ER→ECPN→ESF; efectivo concilia ESF↔EFE.  
`[I]` Editar una celda de “Total Activo” rompería la identidad sin una transacción.

**ALTERNATIVAS:**  
1) Cuatro formularios independientes sincronizados ad hoc.  
2) Un estado de cuentas + proyecciones (elegida).  
3) Grafo de dependencias genérico.

**POR QUÉ:**  
Refleja la contabilidad del curso y simplifica validación A=P+PN y reconciliación de efectivo.

**CONFIANZA:** Alta  

**FUENTE:**  
Park City solucionario; PD4 Sapiense; Las Vegas; PPTX detalle ER (dual ESF+ER).

---

## D06 — No usar grafos como estructura central

**DECISIÓN:**  
Se descartan grafos como arquitectura primaria. Bastan catálogo + plantillas + funciones de proyección + orden de cálculo.

**EVIDENCIA:**  
`[R]` Las dependencias observadas son encadenamientos lineales/formulario (CV, IR, RL, totales).  
`[P]` Un grafo no aporta capacidad de test que no dé una pipeline explícita.

**ALTERNATIVAS:**  
1) Motor de grafos.  
2) Pipeline + reglas declarativas (elegida).  
3) Hojas de cálculo embebidas como motor.

**POR QUÉ:**  
Los grafos añadirían sofisticación sin evidencia de necesidad; dificultan el debugging pedagógico (“qué regla disparó”).

**CONFIANZA:** Alta  

**FUENTE:**  
Hojas de trabajo Park City; solucionarios PD3; requisito de no sobrearquitectura.

---

## D07 — Representación de reglas: YAML/JSON + funciones Python

**DECISIÓN:**  
Catálogo de cuentas, plantillas de estados y tipos de transacción en YAML/JSON; cálculos (dep, IR, tope RL, CV, proyecciones) en funciones Python testeables.

**EVIDENCIA:**  
`[R]` Catálogo grande y estable (Presentación 2, PDF cuentas).  
`[R]` Cálculos con condiciones (tope RL, prorrateos) aparecen en PPTX y solucionarios.  
`[P]` Auditar “¿de dónde salió esta cuenta?” es más fácil en YAML ligado a fuente.

**ALTERNATIVAS:**  
A) Solo funciones Python.  
B) Config estructurada + funciones (elegida).  
C) Solo objetos OO.  
D) Motor de reglas externo (Drools-like).

**POR QUÉ:**  
Equilibrio entre legibilidad frente a materiales y potencia de cálculo; encaja con pytest y fixtures.

**CONFIANZA:** Media-Alta  

**FUENTE:**  
Presentación 2; PDF cuentas ESF; PPTX análisis ESF; PD2 E1; comparación de alternativas del plan.

---

## D08 — EFE del MVP = método directo

**DECISIÓN:**  
Implementar primero EFE por **método directo** (cobros/pagos clasificados en AO/AI/AF). Método indirecto queda aplazado.

**EVIDENCIA:**  
`[R]` PD3 E3, PD4 E1, Las Vegas, Park City usan listados de cobros/pagos.  
`[R]` Cronograma menciona “directo e indirecto”, pero los ejercicios del corpus disponible no desarrollan indirecto.  
`[R]` Presentación 4 nombra ambos métodos sin detallar indirecto en el texto extraído.

**ALTERNATIVAS:**  
1) Ambos métodos en MVP.  
2) Solo directo (elegida).  
3) Solo indirecto.

**POR QUÉ:**  
Sin solucionario de indirecto no hay test golden. Evita reglas inventadas.

**CONFIANZA:** Alta para el MVP · Media para el curso completo  

**FUENTE:**  
PD3/PD4 solucionarios; Las Vegas; Park City; Cronograma Semana 5; Presentación 4.

---

## D09 — Vista integrada 2×2 pospuesta (Fase 8)

**DECISIÓN:**  
No es la interfaz inicial. Primero modos A/B/E (un estado, guiado, comprobar). La vista simultánea de cuatro estados aparece tras integración validada por tests.

**EVIDENCIA:**  
`[R]` Semanas 1–2 y PC1 evalúan ESF aislado.  
`[R]` Integración explícita en PD4 / ejercicios 4 EEFF / PC2 (cronograma).  
`[P]` Principiante se satura con cuatro plantillas a la vez.

**ALTERNATIVAS:**  
1) Home = 2×2 desde el día 1.  
2) Aislado → integración → 2×2 (elegida).  
3) Nunca vista integrada.

**POR QUÉ:**  
Alinea software al cronograma real; reduce riesgo de UI costosa sin aprendizaje.

**CONFIANZA:** Alta  

**FUENTE:**  
Cronograma; PC1; PD1–PD4; crítica sección 13 del plan.

---

## D10 — Interacción = transacciones tipadas, no edición libre de celdas

**DECISIÓN:**  
El simulador aplica operaciones de un catálogo (compra, venta+CV, cobro, aporte, préstamo, etc.). No se permite editar arbitrariamente “Utilidad neta” o “Total activo”.

**EVIDENCIA:**  
`[R]` Enunciados narran transacciones/hechos.  
`[R]` Solucionarios registran filas por operación.  
`[I]` Edición libre genera estados imposibles y no entrena el método del curso.

**ALTERNATIVAS:**  
1) Spreadsheet libre.  
2) Transacciones tipadas (elegida).  
3) Solo rellenar plantillas sin motor de txs.

**POR QUÉ:**  
Conserva partida doble/ecuación y hace explicable el diff antes/después.

**CONFIANZA:** Alta  

**FUENTE:**  
Ejercicios Semana 1–2; PD1 Ej.2; PC1 P2; metodología PD2.

---

## D11 — Stack: Python (motor + FastAPI) + React (Vite) + SQLite/JSON

**DECISIÓN:**  
Backend/motor en Python; API FastAPI; frontend React con Vite; progreso local en SQLite o JSON.

**EVIDENCIA:**  
`[P]` Tests golden y extracción de xlsx son naturales en Python (`pytest`, `openpyxl`).  
`[P]` Prototipo localhost sin sobrearquitectura.  
`[P]` React cubre bien modos A–E y futura vista integrada.

**ALTERNATIVAS:**  
1) React + FastAPI (elegida).  
2) App Python pura (Streamlit/NiceGUI).  
3) Next.js full-stack JS.  
4) Solo Excel/VBA.

**POR QUÉ:**  
El valor está en el motor y los tests; Python maximiza rigor contable. React evita pelear UI compleja en Streamlit a medio plazo. Next.js obligaría a reimplementar el motor en JS o mantener dos lenguajes de dominio.

**CONFIANZA:** Media-Alta  

**FUENTE:**  
Comparación de arquitectura del plan; naturaleza de solucionarios xlsx; requisito localhost educativo.

---

## D12 — Solucionarios como tests golden; no “arreglar” reglas a ciegas

**DECISIÓN:**  
Cada solucionario prioritario se convierte en fixture `input → expected`. Si el motor discrepa, se clasifica la causa (regla / interpretación / contexto / excepción / dato / inconsistencia material) antes de cambiar código.

**EVIDENCIA:**  
`[R]` Existen pares enunciado–solución en Semanas, PDs y PC1.  
`[R]` Park City muestra `#REF!` en una zona → posible inconsistencia del material.  
`[P]` Evita overfitting a un Excel defectuoso.

**ALTERNATIVAS:**  
1) Tests sintéticos inventados.  
2) Golden desde materiales + triage (elegida).  
3) Sin tests automatizados.

**POR QUÉ:**  
Es la única forma de demostrar fidelidad académica sin LLM.

**CONFIANZA:** Alta  

**FUENTE:**  
Todos los solucionarios listados en `INVENTARIO_MATERIALES.md`; Park City solucionario.

---

## D13 — Sistema periódico de mercadería en el MVP

**DECISIÓN:**  
El cálculo de costo de ventas sigue el esquema periódico II + CN − IF (con ajustes que el enunciado indique, p.ej. robo).

**EVIDENCIA:**  
`[R]` Presentación 3 marca “Sistema Periódico (*) Sistema utilizado en el curso”.  
`[R]` Hojas de trabajo Park City / Las Vegas / Chicago usan II, compras, fletes, IF.

**ALTERNATIVAS:**  
1) Inventario permanente como default.  
2) Periódico como default del curso (elegida).  
3) Ambos desde el MVP.

**POR QUÉ:**  
Es la convención explícita del material teórico del curso.

**CONFIANZA:** Alta  

**FUENTE:**  
`Presentación 3 ... ECPN.ppt`; hojas CV Park City/Las Vegas.

---

## D14 — Adaptación por tipos de error: simple y post-MVP UI

**DECISIÓN:**  
Registrar contadores determinísticos por skill/error. Usar umbrales fijos para recomendar ejercicios. Sin machine learning. Implementar tras Modos A/B/E básicos.

**EVIDENCIA:**  
`[R]` El curso distingue clasificación, armado ESF, ER, EFE, integración (PD1→PD4).  
`[P]` Útil, pero no bloquea el aprendizaje del motor.

**ALTERNATIVAS:**  
1) ML personalizado.  
2) Contadores determinísticos (elegida).  
3) Sin adaptación.

**POR QUÉ:**  
Bajo costo, interpretable, alineado a errores reales; evita retrasar el MVP.

**CONFIANZA:** Media  

**FUENTE:**  
Secuencia PD1–PD4; metodología PD2; plan sección 11.

---

## D15 — Materiales originales intocables; docs separados

**DECISIÓN:**  
No modificar `OneDrive_2026-09-11/` ni el zip. Todo análisis vive en `docs/`. El código futuro no se mezcla con los PDF/PPT/XLSX fuente.

**EVIDENCIA:**  
`[P]` Requisito del proyecto.  
`[R]` Corpus ya extraído en carpeta dedicada.

**ALTERNATIVAS:**  
1) Editar solucionarios “para limpiarlos”.  
2) Separación estricta (elegida).

**POR QUÉ:**  
Preserva trazabilidad y evita contaminar la fuente de verdad.

**CONFIANZA:** Alta  

**FUENTE:**  
Requisitos del usuario; layout actual del repo.

---

## D16 — Hallazgos de Presentaciones 1–4 (.ppt) incorporados

**DECISIÓN:**  
Tras extracción COM de las cuatro presentaciones legacy, se confirman/añaden al modelo: (1) lista oficial de 4 EEFF; (2) plantilla y suborden AC disponible/exigible/realizable; (3) sobregiro antes de tributos; (4) ER no acumulativo + CV periódico; (5) EFE con efectivo = caja+bancos+inversiones CP; (6) AO/AI/AF; (7) sinónimo “Estado de Resultados Integrales”.

**EVIDENCIA:**  
`[R]` Texto extraído de Presentaciones 1–4 (sesión de análisis).

**ALTERNATIVAS:**  
1) Ignorar .ppt y basarse solo en PDF/XLSX.  
2) Incorporar (elegida).

**POR QUÉ:**  
Cierra el pendiente del reconocimiento; aporta reglas de presentación y nomenclatura.

**CONFIANZA:** Alta  

**FUENTE:**  
`Semana 1/Presentación 1...ppt`; `Presentación 2...ppt`; `Semana 3 y 4/Presentación 3...ppt`; `Presentación 4...ppt`.

---

## D17 — Tensión “Anticipo de clientes”: resolver con más evidencia antes de hardcodear

**DECISIÓN:**  
No fijar aún una única representación interna. Presentación 2 lo menciona como “activo negativo” bajo exigible; PDF de cuentas y PDs lo tratan como **pasivo** (anticipos recibidos). Hasta reconciliar, el catálogo marcará la cuenta como pasivo (uso dominante en ejercicios) y documentará la nota de Presentación 2 como aclaración pedagógica.

**EVIDENCIA:**  
`[R]` Presentación 2: “Anticipo de clientes (activo negativo)”.  
`[R]` PDF cuentas / PD1 tabla: anticipos recibidos de clientes como Pasivo.  
`[R]` PC1 Sol_P2 expone Anticipo de Clientes en pasivo.

**ALTERNATIVAS:**  
1) Seguir solo Presentación 2.  
2) Seguir ejercicios/PC (pasivo) + nota (elegida).  
3) Soportar ambas presentaciones en UI.

**POR QUÉ:**  
Los solucionarios evaluados (PC1) mandan sobre una diapositiva ambigua para el runtime.

**CONFIANZA:** Media  

**FUENTE:**  
Presentación 2; `2. FC Cuentas del ESF.pdf`; PD1; PC1 Solucionario.

---

## Resumen de confianza

| ID | Tema | Confianza |
|----|------|-----------|
| D01 | Alcance MVP U1–4 | Alta |
| D02 | Fidelidad UP | Alta |
| D03 | Sin LLM runtime | Alta |
| D04 | Ecuación como ledger | Alta |
| D05 | EEFF como proyecciones | Alta |
| D06 | Sin grafos centrales | Alta |
| D07 | YAML + Python | Media-Alta |
| D08 | EFE directo | Alta (MVP) |
| D09 | 2×2 pospuesto | Alta |
| D10 | Transacciones tipadas | Alta |
| D11 | FastAPI + React | Media-Alta |
| D12 | Golden tests | Alta |
| D13 | Sistema periódico | Alta |
| D14 | Adaptación simple | Media |
| D15 | Materiales intocables | Alta |
| D16 | PPT incorporados | Alta |
| D17 | Anticipo clientes | Media |
