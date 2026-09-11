"""Transcripción narrativa de Park City. Valores esperados viven solo en tests."""
from .equation import Ledger
from .transactions import apply_operation
from .closes import depreciation, periodic_cost, prorate
from .projections import project
from .money import ZERO


def park_city():
    ledger=Ledger({'cash':'70000','investments_cp':'80000','receivables':'60000','inventory':'25000','equipment':'150000','dep_equipment':'-7500',
        'tax_payable':'2100','payables':'25000','salaries_payable':'9000','capital':'300000','reserve':'4140','retained':'37260'})
    def op(kind,amount,**extra): apply_operation(ledger,{'type':kind,'amount':amount,**extra})
    def move(deltas,label,activity=None,rule='equation'): ledger.apply(deltas,label,cash_activity=activity,rule_id=rule)
    op('collection','60000')
    move({'cash':'-2100','tax_payable':'-2100'},'Pago de tributos iniciales','AO')
    op('supplier_payment','25000')
    move({'cash':'-9000','salaries_payable':'-9000'},'Pago de sueldos iniciales','AO')
    move({'cash':'470000','receivables':'25000','sales':'500000','sales_returns':'5000'},'Ventas brutas menos rebajas; quedan S/ 25 000 por cobrar','AO','sale')
    move({'inventory':'159000','cash':'-138000','payables':'21000'},'Compras 150 000 + fletes 10 000 − rebajas 1 000','AO','periodic')
    cost=periodic_cost('25000','150000','35000','10000','1000','6000','separate')
    move({'inventory':-cost,'cost':cost},'Costo periódico, robo separado',rule='periodic')
    move({'inventory':'-6000','theft':'6000'},'Robo reportado por almacén',rule='periodic')
    move({'cash':'-48000','prepaid_rent':'12000','prepaid_rent_lp':'36000'},'Alquiler anticipado de cuatro años','AO','prorate')
    consumed=prorate('48000','6','48')
    move({'prepaid_rent_lp':-consumed,'rent_expense':consumed},'Alquiler consumido: julio a diciembre',rule='prorate')
    op('loan','180000');op('loan_payment','10000')
    move({'loan_lp':'-60000','loan_cp':'60000'},'Reclasificación de doce cuotas exigibles el próximo año')
    op('interest','1050',cash_part='700',activity='AF')
    move({'cash':'-55000','vehicles':'55000'},'Compra de vehículo','AI')
    dep=depreciation('55000','5000','10','2')
    move({'dep_vehicles':-dep,'dep_expense':dep},'Vehículo: dos meses según la hoja de trabajo',rule='depreciation')
    move({'dep_equipment':'-15000','dep_expense':'15000'},'Depreciación de IME: 10% anual',rule='depreciation')
    op('salary','34000',cash_part='30000');op('utilities','21000',cash_part='20000')
    move({'allowance':'-1250','bad_debt':'1250'},'Incobrables: 5% del saldo por cobrar')
    op('contribution','65000')
    profit=project(ledger)['ER']['net_profit']
    op('capitalization',str(profit*__import__('decimal').Decimal('.30')))
    op('dividend',str(profit*__import__('decimal').Decimal('.15')))
    # [I] EFE source pays 28,221 while ECPN declares 28,221.15.
    # Preserve actual cash evidence and retain the unpaid 0.15 as a liability.
    op('dividend_payment','28221')
    return ledger


def equation_case1():
    """Semana 1 caso 1, importes de filas 3–15, operaciones tipadas."""
    ledger=Ledger()
    operations=[
        {'type':'contribution','amount':'289000'},
        # Equipment bought on credit and property purchase require internal facts.
    ]
    for operation in operations: apply_operation(ledger,operation)
    ledger.apply({'equipment':'2000','other_payables':'2000'},'Equipos al crédito')
    ledger.apply({'cash':'-40000','buildings':'40000'},'Compra de inmueble',cash_activity='AI')
    for op in [
        {'type':'purchase','amount':'15500','cash_part':'15500'},
        {'type':'sale','amount':'8000','cash_part':'0','cost':'3000'},
        {'type':'collection','amount':'8000'}]: apply_operation(ledger,op)
    ledger.apply({'cash':'-2000','other_payables':'-2000'},'Pago de equipos',cash_activity='AI')
    apply_operation(ledger,{'type':'sale','amount':'12000','cash_part':'12000','cost':'2500'})
    apply_operation(ledger,{'type':'utilities','amount':'600','cash_part':'0'})
    apply_operation(ledger,{'type':'salary','amount':'4000','cash_part':'3400'})
    return ledger
