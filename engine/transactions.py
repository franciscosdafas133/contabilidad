from .catalog import read_knowledge
from .money import ZERO, AccountingError, positive


def apply_operation(ledger, operation):
    kind=operation.get('type')
    definitions={x['id']:x for x in read_knowledge('transaction_types')}
    if kind not in definitions: raise AccountingError('Tipo de operación desconocido.')
    spec=definitions[kind]
    required={'type',*spec['fields']}
    allowed=required|{'label'}
    if set(operation)-allowed: raise AccountingError('La operación contiene campos no permitidos.')
    if required-set(operation): raise AccountingError('Faltan datos para aplicar la operación.')
    amount=positive(operation['amount'])
    paid=positive(operation['cash_part'],True) if 'cash_part' in operation else ZERO
    if paid>amount: raise AccountingError('La parte al contado supera el importe total.')
    activity=None;rule='equation'
    if kind=='contribution': deltas={'cash':amount,'capital':amount};activity='AF'
    elif kind=='asset_contribution': deltas={'equipment':amount,'capital':amount};rule='noncash'
    elif kind=='purchase': deltas={'inventory':amount,'cash':-paid,'payables':amount-paid};activity='AO' if paid else None
    elif kind=='sale':
        cost=positive(operation['cost'],True)
        deltas={'cash':paid,'receivables':amount-paid,'sales':amount,'inventory':-cost,'cost':cost};activity='AO' if paid else None;rule='sale'
    elif kind=='collection': deltas={'cash':amount,'receivables':-amount};activity='AO'
    elif kind=='supplier_payment': deltas={'cash':-amount,'payables':-amount};activity='AO'
    elif kind=='loan': deltas={'cash':amount,'loan_lp':amount};activity='AF'
    elif kind=='loan_payment': deltas={'cash':-amount,'loan_lp':-amount};activity='AF'
    elif kind=='equipment_purchase': deltas={'cash':-amount,'equipment':amount};activity='AI'
    elif kind in ('salary','utilities','interest'):
        expense,payable={'salary':('salary_expense','salaries_payable'),'utilities':('utilities','other_payables'),'interest':('interest_expense','interest_payable')}[kind]
        deltas={expense:amount,'cash':-paid,payable:amount-paid}
        if kind=='interest' and operation['activity'] not in ('AO','AF'):
            raise AccountingError('Indique AO o AF para los intereses según el caso.')
        activity=(operation['activity'] if kind=='interest' else 'AO') if paid else None
    elif kind=='dividend': deltas={'retained':-amount,'dividends_payable':amount};rule='noncash'
    elif kind=='dividend_payment': deltas={'cash':-amount,'dividends_payable':-amount};activity='AF'
    elif kind=='capitalization': deltas={'retained':-amount,'capital':amount};rule='ecpn'
    return ledger.apply(deltas,operation.get('label') or spec['label'],cash_activity=activity,rule_id=rule)

