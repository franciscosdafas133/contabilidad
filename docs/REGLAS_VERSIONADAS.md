# Catálogo y reglas — versión 1

Implementación de fases 0–8 del plan. Fuente académica: corpus local; no son recomendaciones tributarias actuales. El runtime no consulta servicios externos ni LLM.

`knowledge/accounts.json`, `rules.json`, `statement_templates.json` y `transaction_types.json` contienen la transcripción legible y sus referencias. `scripts/build_knowledge.py` permite regenerarla.

## Convenciones

- [R] Los saldos de contra-activos se representan negativos; conservan su elemento Activo. La validación usa A + G = P + PN + I durante el período.
- [P] Precisión interna Decimal (28 dígitos), sin redondear cada operación. Presentación a dos decimales, ROUND_HALF_UP. Los golden comparan valores internos con tolerancia absoluta 0,000001 por los decimales binarios del Excel. No se usa esa tolerancia para ocultar diferencias materiales.
- [P] Una pérdida no genera crédito fiscal automático y no transfiere reserva. No se modelan impuestos diferidos.
- [R] IR y reserva solo se aplican si el ejercicio pide cierre. Super Smash usa 30% (hoja impuesto C4), PC1/PD3/Park City usan 29,5%. No aplicar cierres anuales al ejercicio mensual PD2 E2.
- [R] Meses/días consumidos son parámetros del enunciado; no inferirlos únicamente de una fecha de adquisición. PD2 E1 K10:K13 aporta 69, 29, 55 y 11 meses.
- [R] CV periódico, con robo separado en Park City y Las Vegas. El tipo venta admite costo conocido para las matrices iniciales del curso. No ejecutar ambos sobre la misma venta.
- [R] Intereses pagados AF en Park City/Las Vegas; selección explícita por caso en la operación, sin regla universal.
- [R] Anticipos de clientes como Pasivo según PD1/PC1; conservar nota D17 del plan.
- [P] Las inversiones CP son una línea separada. Solo son equivalentes de efectivo si el caso las identifica expresamente. No asumir que acciones de PD2 son efectivo.
- [P] No se permiten depreciaciones superiores al costo menos rescate ni operaciones que produzcan inventario/deudas negativos. Efectivo negativo se presenta como sobregiro sin mutar el saldo de origen.
- [P] Simulación local con operaciones tipadas; las matrices internas de fixtures no son una API pública de edición arbitraria.

## Alcance verificable

El catálogo es un subconjunto operativo de U1–4 con 62 cuentas; no pretende ser un plan contable nacional completo. Pruebas sintéticas prueban límites y rechazo de entradas; los resultados académicos deben tener celdas golden independientes. La simulación no sustituye un piloto pedagógico.
