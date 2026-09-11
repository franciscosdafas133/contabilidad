# Discrepancias de los materiales

No se modifica el corpus. Estas observaciones se verifican mediante pruebas de regresión.

| ID | Fuente y celdas | Hallazgo | Tratamiento |
|---|---|---|---|
| SS-01 | Super Smash, impuesto C3:C5 | Tasa histórica del 30%, no 29,5%. UAIR 468 600; IR 140 580. | Parámetro específico 0,30. Matriz, cierre y ESF pasan sin excepción numérica. |
| PC-01 | PC1 Sol_P1 L10:L11; Sol_P2 T22 | Importes con más de dos decimales: 2 986,875 y 52,875. | Mantener Decimal sin redondeo intermedio; mostrar dos decimales. No adoptar redondeo por operación. |
| PARK-01 | Park City, EEFF Solución L83/L85 | `#REF!` en un bloque auxiliar duplicado. | Excluir solo ese bloque; usar F71/F75/F82/F88, que sí concilian. |
| PARK-02 | C56/C111; F51/E111; H52/F81 | Depreciación ER 833,333… frente a ESF 833; capitalización 56 442,30 frente a 56 442; dividendos declarados 28 221,15 frente a pagados 28 221. | Integración coherente: mantener decimales de ER/ECPN y el efectivo de EFE; reconocer S/ 0,15 de dividendos pendientes [I]. La interfaz lo informa. No afirmar que todo el ESF original coincide. |
| PARK-03 | E113 frente a H53 | Resultados acumulados ESF 121 924,2333… frente a ECPN 121 923,45. | Se usa el ECPN coherente con ER. Total activo recalculado 841 395,6666… (841 395,67 visible). El total 841 396 del Excel no es golden estricto. |
| PARK-04 | Hoja de trabajo B24/B53 | Fechas auxiliares 2021 frente al enunciado 2020. | Seguir el período narrativo 2020 y meses explícitos, no inferir fechas. |
| PD4-01 | Pregunta 2- sol C23/F23/F24/G24 | Diferencia de S/ 0,30 reconocida por el solucionario; impuesto F9 redondeado frente a G9. | No usar como golden integrado en equilibrio. La prueba exige detectar la diferencia. |
| PD4-02 | Pregunta 2- sol P34/P44/P45/P46 | Cobro de venta de terreno vacío; flujo neto −245 342 no concilia con efectivo inicial 13 560 y final 47 030. | Dato faltante. Cobro inferido 278 812 [I], no se presenta como respuesta oficial. PD4 Terracan sí es golden completo de EFE. |

La cobertura integrada usa Park City: celdas limpias de los cuatro estados y reconciliaciones calculadas de forma independiente. No se amplía la tolerancia global para hacer pasar estas discrepancias. Las diferencias de representación de dos decimales se distinguen de los saldos internos.
