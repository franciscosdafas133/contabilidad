from copy import deepcopy
from .catalog import read_knowledge, accounts
from .equation import Ledger
from .projections import er, efe, ecpn, esf
from .closes import income_tax, legal_reserve
from .money import ZERO, AccountingError


def get_exercise(id):
    for ex in read_knowledge('exercises'):
        if ex['id']==id: return ex
    raise KeyError(id)


def public_exercise(ex):
    result=deepcopy(ex)
    if result['kind']=='efe':
        for flow in result['data']['flows']: flow.pop('activity')
    if result['kind']=='matrix':
        for row in result['data']['rows']: row.pop('deltas')
    return result


def solve(ex):
    kind=ex['kind'];data=ex['data']
    if kind=='classification': return {k:accounts()[k]['element'] for k in data['accounts']}
    if kind=='er': return er(**data)
    if kind=='ecpn': return ecpn(**data)
    if kind=='efe': return {**efe(**data),**{f'flow_{i}':f['activity'] for i,f in enumerate(data['flows'])}}
    if kind=='matrix':
        ledger=Ledger(data['opening']);initial=ledger.balances.get('retained',ZERO)
        for row in data['rows']:
            ledger.apply(row['deltas'],row['label'],cash_activity='AO' if row['deltas'].get('cash') else None)
        if data.get('closing'):
            profit=ledger.balances.get('retained',ZERO)-initial
            tax=income_tax(profit,data['closing']['tax_rate'])
            reserve=legal_reserve(profit-tax,ledger.balances.get('capital',ZERO),ledger.balances.get('reserve',ZERO))
            if tax: ledger.apply({'tax_payable':tax,'retained':-tax},'Impuesto')
            if reserve: ledger.apply({'reserve':reserve,'retained':-reserve},'Reserva')
        return {**{k:ledger.balances.get(k,ZERO) for k in data['rows'][0]['deltas']},**ledger.balances,
            **{f'section_{k}':a['section'] for k,a in accounts().items()},'statement':esf(ledger.balances),'trace':ledger.history}
    raise AccountingError('Ejercicio no soportado.')
