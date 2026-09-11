"""Prepare public learning inputs, never export golden answers."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
accounts={a['id']:a for a in json.loads((ROOT/'knowledge/accounts.json').read_text(encoding='utf-8'))}
specs=[
 ('pd1_clasificacion','PD1 · Reconocer las cuentas','classification','Clasifica cada cuenta por su elemento contable.','2026'),
 ('semana1_caso1','Semana 1 · Ecuación contable','equation','Registra los hechos en la ecuación contable y determina los saldos finales.','Caso 1'),
 ('pd1_ecuacion','PD1 · BikeAndes','equation','Construye la ecuación con las operaciones de BikeAndes y determina los saldos finales.','Agosto a diciembre de 2026'),
 ('pd2_esf','PD2 · DEF S.A.C.','esf','Prepara el ESF al 31 de julio; incluye depreciación y amortización. Este caso no pide cierre anual.','Al 31 de julio de 2026'),
 ('pd3_er','PD3 · EXA PERÚ S.A.C.','er','Construye el Estado de Resultados a partir de los ingresos y gastos. IR: 29,5%.','Del 1 de enero al 31 de diciembre de 2026'),
 ('pd3_ecpn','PD3 · EL NIÑO S.A.C.','ecpn','Elabora el ECPN. Los dividendos de S/ 80 000 se pagan en marzo de 2027; aquí se reconocen al declararse. Reserva legal: 10%, tope 20% del capital.','Del 1 de enero al 31 de diciembre de 2026'),
 ('pd3_efe','PD3 · BCB S.A.C.','efe','Clasifica los cobros y pagos en AO, AI y AF, y calcula el efectivo final.','Del 1 de enero al 31 de diciembre de 2026'),
 ('pd4_terracan','PD4 · TERRACAN S.A.','efe','Prepara el EFE directo. Los aportes en equipos y los dividendos no pagados no generan flujo.','Del 1 de enero al 31 de diciembre de 2026'),
 ('poder_er','Ejemplo · PODER SAC','er','Construye el ER y calcula el impuesto a la renta con tasa de 29,5%.','Del 1 de enero al 31 de diciembre de 2021'),
 ('las_vegas_er','Las Vegas · Estado de Resultados','er','Construye el ER. El CV de 890 000 excluye el robo de 5 000, presentado como pérdida operativa.','Del 1 de enero al 31 de diciembre de 2020'),
 ('las_vegas_efe','Las Vegas · Flujos de efectivo','efe','Elabora el EFE. En este solucionario los intereses pagados se clasifican como financiamiento.','Del 1 de enero al 31 de diciembre de 2020'),
 ('valparaiso_ecpn','Valparaíso · Cambios patrimoniales','ecpn','Reconoce aportes, reinversión, reservas y dividendos.','Del 1 de enero al 31 de diciembre'),
]
labels={'net_sales':'Ventas netas','cost':'Costo de ventas (importe)','gross_profit':'Utilidad bruta','operating_profit':'Utilidad operativa','profit_before_tax':'Utilidad antes del impuesto','tax':'Impuesto a la renta (importe)','net_profit':'Utilidad neta','capital':'Capital social','reserve':'Reserva legal','voluntary_reserve':'Reserva facultativa','retained':'Resultados acumulados','total':'Total patrimonio neto','AO':'Flujo de operación','AI':'Flujo de inversión','AF':'Flujo de financiamiento','change':'Variación neta de efectivo','final':'Efectivo final'}
rules={'classification':'classification','equation':'equation','esf':'esf','er':'er','ecpn':'ecpn','efe':'efe'}
exercises=[]
prompts={
 'semana1_caso1':[
 'Los socios aportan S/ 289 000 en efectivo.',
 'Se adquieren equipos por S/ 2 000 al crédito (cuentas por pagar diversas).',
 'Se compra un inmueble al contado por S/ 40 000.',
 'Se compra mercadería al contado por S/ 15 000.',
 'Se paga un flete de S/ 500 atribuible a la compra de mercadería.',
 'Se vende al crédito por S/ 8 000. Registra primero el ingreso en resultados acumulados.',
 'La mercadería de la venta anterior tuvo un costo de S/ 3 000. Registra su salida y el costo.',
 'Se cobra la cuenta por cobrar de S/ 8 000.',
 'Se paga la deuda por equipos de S/ 2 000.',
 'Se realiza una venta al contado por S/ 12 000. Registra el ingreso.',
 'El costo de la venta anterior es S/ 2 500. Registra su salida y el costo.',
 'Se reconoce un gasto de S/ 600 pendiente de pago en cuentas por pagar diversas.',
 'El gasto de remuneraciones es S/ 4 000; se pagan S/ 3 400 y quedan S/ 600 pendientes.'
 ],
 'pd1_ecuacion':[
 'Aporte inicial: efectivo S/ 200 000, mercadería S/ 50 000 y vehículos S/ 100 000.',
 'Se reconoce alquiler anticipado de S/ 24 000 y su obligación por pagar diversa.',
 'Se pagan los S/ 24 000 de alquiler anticipado.',
 'Compra de mercadería de S/ 120 000 al crédito.',
 'Se paga el 40% de la compra de mercadería anterior.',
 'Compra de una marca (intangible) por S/ 40 000 al crédito en cuentas diversas.',
 'Se paga la compra de la marca por S/ 40 000.',
 'Compra de muebles y equipos por S/ 45 000 al crédito en cuentas diversas.',
 'Se paga el saldo pendiente de la compra de mercadería de S/ 120 000.',
 'Venta de mercadería por S/ 50 000 al crédito. Registra el ingreso.',
 'Se cobra el 70% de la venta de S/ 50 000.',
 'El costo de esa venta es S/ 10 000.',
 'Se reconoce seguro pagado por adelantado de S/ 9 600, aún pendiente en cuentas diversas.',
 'Se recibe un préstamo de S/ 180 000 en efectivo.',
 'Se cobra el saldo restante de la venta de S/ 50 000.',
 'Nueva venta por S/ 65 000 al crédito. Registra el ingreso.',
 'Se cobra la venta de S/ 65 000.',
 'El costo de esta venta es S/ 39 000.',
 'Nuevo aporte de socios en efectivo de S/ 80 000.',
 'Venta por S/ 55 000 al crédito. Registra el ingreso.',
 'Se cobra el 30% de la venta de S/ 55 000.',
 'El costo de esta venta es S/ 20 000.',
 'Se compran inversiones en valores por S/ 35 000 al contado.',
 'Servicios LAT de agosto a diciembre: S/ 850 por mes, aún pendientes de pago.',
 'Se pagan íntegramente los servicios LAT anteriores.',
 'Sueldos de agosto a diciembre: S/ 4 500 por mes, aún pendientes de pago.',
 'Se pagan cuatro meses de los sueldos anteriores; un mes queda pendiente.'
 ],
 'pd2_esf':[
 'Tres socios aportan S/ 50 000 en efectivo cada uno.',
 'Compra de mercadería de S/ 75 000 al crédito.',
 'Se paga el 30% de la compra de mercadería.',
 'Compra de software por S/ 20 000 al crédito en cuentas diversas.',
 'Venta por S/ 130 000 al crédito. Registra el ingreso.',
 'Se cobra el 40% de la venta de S/ 130 000.',
 'El costo de la venta equivale al 45% de su precio.',
 'Se compran dos equipos de cómputo a S/ 4 500 cada uno, al crédito en cuentas diversas.',
 'Se paga la compra de ambos equipos.',
 'Se devuelve un equipo de S/ 4 500 y se recibe una nota de crédito como anticipo a proveedores.',
 'Se cobra el 50% del saldo pendiente de la venta.',
 'Se reconocen inversiones en valores CP de S/ 65 000 y la obligación en cuentas diversas.',
 'Se pagan las inversiones de S/ 65 000.',
 'Se compra mercadería por S/ 80 000 al crédito.',
 'Amortiza un mes del software de S/ 20 000; vida útil cuatro años.',
 'Deprecia un mes del equipo de S/ 4 500 que se conserva; vida útil tres años, sin rescate.'
 ]}
for id,title,skill,prompt,period in specs:
    f=json.loads((ROOT/f'tests/fixtures/{id}.json').read_text(encoding='utf-8'))
    if id in prompts:
        assert len(prompts[id])==len(f['input']['rows']),id
        for row,prompt_text in zip(f['input']['rows'],prompts[id]): row['prompt']=prompt_text
    tasks=[]
    for key in f['expected']:
        tasks.append({'id':key,'label':accounts[key]['name'] if f['kind'] in ('matrix','classification') else labels[key],
            'type':'choice' if skill=='classification' else 'number','options':['Activo','Pasivo','Patrimonio Neto','Ingreso','Gasto'] if skill=='classification' else [],'rule_id':rules[skill],'skill':skill})
    # EFE classifications are graded separately from arithmetic, without exposing labels in public data.
    if f['kind']=='efe':
        for i,flow in enumerate(f['input']['flows']):
            tasks.insert(i,{'id':f'flow_{i}','label':flow['label'],'type':'choice','options':['AO','AI','AF'],'rule_id':'efe','skill':'efe'})
    if f['kind']=='matrix' and skill=='esf':
        for key in f['expected']:
            tasks.append({'id':f'section_{key}','label':accounts[key]['name']+' · sección','type':'choice','options':['AC','ANC','PC','PNC','PN'],'rule_id':'esf','skill':'esf'})
    exercises.append({'id':id,'title':title,'skill':skill,'prompt':prompt,'period':period,'source':f['source'].split('Fundamentos de Contabilidad/')[-1]+' · '+f['sheet'],
        'kind':f['kind'],'data':f['input'],'tasks':tasks})
(ROOT/'knowledge/exercises.json').write_text(json.dumps(exercises,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'{len(exercises)} ejercicios públicos; PC1 excluido.')
