"""Versioned catalog transcription; evidence references are intentionally explicit."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'knowledge'
OUT.mkdir(exist_ok=True)

def write(name, value):
    (OUT / f'{name}.json').write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')

groups = {
    'AC': [('cash','Efectivo'),('investments_cp','Inversiones en valores de corto plazo'),('receivables','Cuentas por cobrar comerciales'),('notes_receivable','Letras por cobrar'),('other_receivables','Cuentas por cobrar diversas'),('staff_receivables','Cuentas por cobrar al personal'),('allowance','Estimación para cuentas de cobranza dudosa'),('inventory','Mercadería'),('inventory_transit','Mercadería en tránsito'),('supplier_advance','Anticipos a proveedores'),('prepaid_rent','Alquileres pagados por adelantado corto plazo'),('prepaid_insurance','Seguros pagados por anticipado')],
    'ANC': [('investments_lp','Inversiones en valores de largo plazo'),('land','Terrenos'),('buildings','Edificaciones'),('dep_buildings','Depreciación acumulada de edificaciones'),('equipment','Maquinarias y equipos'),('dep_equipment','Depreciación acumulada de maquinarias y equipos'),('furniture','Muebles y enseres'),('dep_furniture','Depreciación acumulada de muebles y enseres'),('vehicles','Vehículos'),('dep_vehicles','Depreciación acumulada de vehículos'),('intangibles','Intangibles'),('amort_intangibles','Amortización acumulada de intangibles'),('prepaid_rent_lp','Alquileres pagados por adelantado largo plazo')],
    'PC': [('overdraft','Sobregiro bancario'),('tax_payable','Tributos por pagar'),('salaries_payable','Sueldos por pagar'),('benefits_payable','Beneficios sociales por pagar'),('payables','Cuentas por pagar comerciales'),('other_payables','Cuentas por pagar diversas'),('customer_advance','Anticipos recibidos de clientes'),('dividends_payable','Dividendos por pagar'),('interest_payable','Intereses por pagar'),('loan_cp','Préstamo por pagar corto plazo')],
    'PNC': [('loan_lp','Préstamo por pagar largo plazo')],
    'PN': [('capital','Capital social'),('reserve','Reserva legal'),('voluntary_reserve','Reserva facultativa'),('retained','Resultados acumulados')],
    'sales': [('sales','Ventas brutas')],
    'deductions': [('sales_returns','Devoluciones y rebajas sobre ventas'),('sales_discount','Descuento por pronto pago otorgado')],
    'cost': [('cost','Costo de ventas')],
    'operating': [('salary_expense','Gastos de sueldos'),('benefits_expense','Gasto por beneficios sociales'),('utilities','Gastos de luz, agua y teléfono'),('rent_expense','Gasto por alquileres'),('insurance_expense','Gasto por seguros'),('dep_expense','Gasto por depreciación'),('amort_expense','Gasto por amortización'),('bad_debt','Gasto por incobrables'),('theft','Pérdida por robo de mercadería'),('donation_expense','Gasto por donaciones'),('marketing','Gasto por marketing y publicidad'),('operating_expense','Otros gastos operativos'),('asset_gain','Utilidad en venta de activo fijo'),('donation_income','Ingreso por donaciones'),('service_income','Ingresos por servicios de asesoría')],
    'financial': [('interest_expense','Gasto por intereses'),('interest_income','Ingreso por intereses'),('exchange_income','Ingreso por ganancia en cambio')],
}
income = {'sales','asset_gain','donation_income','service_income','interest_income','exchange_income'}
catalog=[]
for group, entries in groups.items():
    for index,(key,name) in enumerate(entries):
        element = 'Activo' if group in ('AC','ANC') else 'Pasivo' if group in ('PC','PNC') else 'Patrimonio Neto' if group == 'PN' else 'Ingreso' if key in income else 'Gasto'
        contra = key.startswith(('dep_','amort_')) and group=='ANC' or key=='allowance'
        catalog.append({'id':key,'name':name,'element':element,'section':group,'order':index,'contra':contra,'natural_sign':-1 if contra else 1,
            'source':'Presentación 2 / PDF Cuentas del ESF; PD2 E3' if group in ('AC','ANC','PC','PNC','PN') else 'Presentación 3; PD3 E1 ER; Ejemplo de ER',
            'evidence':'R','note':'D17: se usa Pasivo según PD1 y PC1; la presentación 2 contiene otra nomenclatura.' if key=='customer_advance' else ''})
write('accounts',catalog)
rules = {
 'equation':('Cada operación conserva Activo + Gasto = Pasivo + Patrimonio Neto + Ingreso.','Semana 1, Ejercicio 2; PD1 Ejercicio 2'),
 'classification':('Clasifica por elemento; una contra-cuenta mantiene el elemento y resta en su sección.','PD1 Ejercicio 1; PD2 E3'),
 'esf':('Presenta AC, ANC, PC, PNC y PN; el efectivo negativo se reclasifica como sobregiro.','Presentación 2; PD2 E3'),
 'sale':('La venta reconoce el ingreso; el costo se reconoce por separado cuando el enunciado lo proporciona.','Semana 1 Ejercicio 2; PD1 Ejercicio 2'),
 'periodic':('Costo de ventas = inventario inicial + compras netas − inventario final; separa el robo solo cuando lo pide el caso.','Presentación 3; Park City hoja de trabajo C4:C9; Las Vegas H8:H12'),
 'depreciation':('Depreciación = (costo − rescate) / vida útil × fracción de período. El terreno no se deprecia.','PD2 E1 H3:H7; PPTX Análisis adicional ESF'),
 'amortization':('La amortización del intangible se prorratea sin valor de rescate.','PD2 E2 K17; PPTX Análisis adicional ESF'),
 'prorate':('Reconoce como gasto únicamente la parte consumida del pago anticipado.','PC1 Sol_P1 L7; Park City hoja de trabajo C14:C19'),
 'tax':('Calcula el impuesto con la tasa indicada por el ejercicio sobre la utilidad antes del impuesto.','PC1 Sol_P1 L10; PD3 E1 G40; Super Smash impuesto C4'),
 'reserve':('La transferencia es 10% de la utilidad neta, limitada al espacio hasta 20% del capital.','PPTX Análisis adicional ESF; PD3 E2 ECPTN D32'),
 'er':('Ventas netas menos costo y gastos, más otros ingresos, determinan la utilidad antes de impuestos.','PD3 E1 ER G15:G41; Ejemplo de ER'),
 'ecpn':('Aportes, utilidad, reservas, capitalización y dividendos explican el cambio patrimonial.','PD3 E2 ECPTN B24:F30; Valparaíso C10:F17'),
 'efe':('El EFE directo registra cobros y pagos AO/AI/AF; el devengado no es un flujo.','Presentación 4; PD3 E3 EFE; PD4 Pregunta 1 C23'),
 'noncash':('Los aportes en activos y dividendos pendientes no producen efectivo.','PD4 Pregunta 1 D23; PD3 Ejercicio 2 enunciado'),
 'relationship':('La utilidad del ER alimenta el ECPN; el efectivo del EFE debe conciliar con el ESF.','Park City EEFF Solución; PD4 Pregunta 2'),
}
write('rules',{k:{'text':v[0],'source':v[1],'evidence':'R'} for k,v in rules.items()})
write('statement_templates',{'ESF':{'title':'Estado de Situación Financiera','sections':['AC','ANC','PC','PNC','PN'],'time':'Al'},'ER':{'title':'Estado de Resultados','sections':['sales','deductions','cost','operating','financial','tax'],'time':'Del'},'ECPN':{'title':'Estado de Cambios en el Patrimonio Neto','sections':['capital','reserve','voluntary_reserve','retained'],'time':'Del'},'EFE':{'title':'Estado de Flujos de Efectivo','sections':['AO','AI','AF'],'time':'Del'}})
types = [('contribution','Aporte en efectivo','amount'),('asset_contribution','Aporte en equipos','amount'),('purchase','Compra de mercadería','amount,cash_part'),('sale','Venta con costo indicado','amount,cash_part,cost'),('collection','Cobro a clientes','amount'),('supplier_payment','Pago a proveedores','amount'),('loan','Préstamo recibido','amount'),('loan_payment','Pago de préstamo','amount'),('equipment_purchase','Compra de equipos al contado','amount'),('salary','Gasto de sueldos','amount,cash_part'),('utilities','Gasto de servicios LAT','amount,cash_part'),('interest','Gasto por intereses','amount,cash_part,activity'),('dividend','Declaración de dividendos','amount'),('dividend_payment','Pago de dividendos declarados','amount'),('capitalization','Capitalización de utilidades','amount')]
write('transaction_types',[{'id':key,'label':label,'fields':fields.split(','),'source':'PD1 Ejercicio 2; PC1 Sol_P2; Park City; PD4'} for key,label,fields in types])
print(f'{len(catalog)} cuentas, {len(rules)} reglas y {len(types)} operaciones.')
