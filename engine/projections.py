from copy import deepcopy
from .catalog import accounts, trace
from .closes import income_tax, legal_reserve
from .money import ZERO, EPSILON, AccountingError, number


def er(balances, tax_rate='0.295', close=True):
    catalog=accounts()
    totals={key:ZERO for key in ('sales','deductions','cost','operating','financial')}
    lines=[]
    for key,raw in balances.items():
        if key not in catalog:
            raise AccountingError(f'Cuenta desconocida: {key}')
        a=catalog[key]; value=number(raw)
        if a['section'] in totals:
            if value<0: raise AccountingError('Los ingresos y gastos de entrada deben ser magnitudes positivas.')
            signed=value if a['element']=='Ingreso' else -value
            totals[a['section']]+=signed
            if value: lines.append({'id':key,'name':a['name'],'section':a['section'],'amount':signed})
    net_sales=totals['sales']+totals['deductions']
    gross=net_sales+totals['cost']
    operating=gross+totals['operating']
    profit=operating+totals['financial']
    tax=income_tax(profit,tax_rate) if close else ZERO
    return {'lines':lines,'net_sales':net_sales,'cost':-totals['cost'],'gross_profit':gross,
            'operating_profit':operating,'profit_before_tax':profit,'tax':tax,'tax_expense':-tax,'net_profit':profit-tax}


def efe(initial, flows):
    totals={key:ZERO for key in ('AO','AI','AF')}
    clean=[]
    for flow in flows:
        if flow['activity'] not in totals:
            raise AccountingError('Actividad EFE desconocida.')
        amount=number(flow['amount'])
        totals[flow['activity']]+=amount
        clean.append({**flow,'amount':amount})
    change=sum(totals.values(),ZERO)
    return {**totals,'initial':number(initial),'change':change,'final':number(initial)+change,'lines':clean}


def ecpn(opening, profit, contribution='0', capitalization='0', voluntary='0', dividends='0', reserve_rate='0.10', cap_rate='0.20'):
    keys=['capital','reserve','voluntary_reserve','retained']
    if set(opening)-set(keys): raise AccountingError('Cuenta patrimonial desconocida.')
    base={k:number(opening.get(k,'0')) for k in keys}
    changes={k:number(v) for k,v in dict(contribution=contribution,capitalization=capitalization,voluntary=voluntary,dividends=dividends).items()}
    if any(v<0 for v in changes.values()): raise AccountingError('Los movimientos patrimoniales deben ser positivos.')
    capital=base['capital']+changes['contribution']+changes['capitalization']
    reserve=legal_reserve(profit,capital,base['reserve'],reserve_rate,cap_rate)
    rows=[{'label':'Saldo inicial',**base},
          {'label':'Aportes','capital':changes['contribution']},
          {'label':'Utilidad del ejercicio','retained':number(profit)},
          {'label':'Capitalización','capital':changes['capitalization'],'retained':-changes['capitalization']},
          {'label':'Transferencia a reserva legal','reserve':reserve,'retained':-reserve},
          {'label':'Reserva facultativa','voluntary_reserve':changes['voluntary'],'retained':-changes['voluntary']},
          {'label':'Dividendos declarados','retained':-changes['dividends']}]
    final={k:sum((r.get(k,ZERO) for r in rows),ZERO) for k in keys}
    return {**final,'total':sum(final.values(),ZERO),'transfer':reserve,'rows':rows}


def esf(balances):
    catalog=accounts(); values={k:number(v) for k,v in balances.items()}
    if values.get('cash',ZERO)<0:
        values['overdraft']=values.get('overdraft',ZERO)-values['cash'];values['cash']=ZERO
    sections={k:[] for k in ('AC','ANC','PC','PNC','PN')}
    for key,value in values.items():
        if key not in catalog: raise AccountingError(f'Cuenta desconocida: {key}')
        a=catalog[key]
        if a['section'] in sections and value:
            sections[a['section']].append({'id':key,'name':a['name'],'amount':value,'order':a['order'],'contra':a['contra']})
    for lines in sections.values(): lines.sort(key=lambda row:row['order'])
    totals={k:sum((line['amount'] for line in v),ZERO) for k,v in sections.items()}
    assets=totals['AC']+totals['ANC'];liabilities=totals['PC']+totals['PNC']
    difference=assets-liabilities-totals['PN']
    return {'sections':sections,'totals':totals,'assets':assets,'liabilities':liabilities,
            'equity':totals['PN'],'liabilities_equity':liabilities+totals['PN'],'difference':difference,'balanced':abs(difference)<=EPSILON}


def project(ledger, *, close=True, reserve=True, tax_rate='0.295', reserve_rate='0.10', cap_rate='0.20'):
    """Pure projection: calling twice never compounds tax/profit/reserve."""
    result_er=er(ledger.balances,tax_rate,close)
    balances=deepcopy(ledger.balances)
    net=result_er['net_profit']
    transfer=legal_reserve(net,balances.get('capital',ZERO),balances.get('reserve',ZERO),reserve_rate,cap_rate) if reserve and close else ZERO
    balances['tax_payable']=balances.get('tax_payable',ZERO)+result_er['tax']
    balances['retained']=balances.get('retained',ZERO)+net-transfer
    balances['reserve']=balances.get('reserve',ZERO)+transfer
    result_esf=esf(balances)
    result_efe=efe(ledger.opening.get('cash',ZERO),ledger.flows)
    keys=['capital','reserve','voluntary_reserve','retained']
    rows=[{'label':'Saldo inicial',**{k:ledger.opening.get(k,ZERO) for k in keys}}]
    for item in ledger.history:
        movements={k:v for k,v in item['deltas'].items() if k in keys}
        if movements: rows.append({'label':item['label'],**movements})
    rows.extend([{'label':'Utilidad del ejercicio','retained':net},{'label':'Reserva legal del período','reserve':transfer,'retained':-transfer}])
    equity={k:balances.get(k,ZERO) for k in keys}
    result_ecpn={**equity,'total':sum(equity.values(),ZERO),'rows':rows,'transfer':transfer}
    cash_difference=result_efe['final']-ledger.balances.get('cash',ZERO)
    traces=list(ledger.history)+[
        trace('er',ledger.balances,result_er,['ER']),
        trace('tax',{'profit':result_er['profit_before_tax'],'rate':tax_rate,'enabled':close},result_er['tax'],['ER.tax','ESF.tax_payable']),
        trace('reserve',{'net_profit':net,'capital':balances.get('capital',ZERO),'enabled':reserve and close},transfer,['ECPN.reserve','ESF.reserve']),
        trace('relationship',{'net_profit':net,'cash_final':result_efe['final']},{'equation_difference':result_esf['difference'],'cash_difference':cash_difference},['ER','ECPN','ESF','EFE'])]
    return {'ER':result_er,'ESF':result_esf,'ECPN':result_ecpn,'EFE':result_efe,'balances':balances,
            'checks':{'equation':result_esf['balanced'],'cash':abs(cash_difference)<=EPSILON,
                      'equity':abs(result_ecpn['total']-result_esf['equity'])<=EPSILON},'trace':traces}
