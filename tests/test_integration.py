from decimal import Decimal
from engine.catalog import ROOT
from engine.scenarios import park_city
from engine.projections import project
from engine.transactions import apply_operation
import json


def test_park_city_clean_cells_across_four_statements():
    evidence=json.loads((ROOT/'docs/evidence/solucionario Ejercicio  (4 Estados Financieros ) Cia Park City (2).json').read_text(encoding='utf-8'))
    source=evidence['sheets']['EEFF Solución']
    result=project(park_city())
    refs={'ER.net_sales':'C50','ER.cost':'C51','ER.gross_profit':'C52','ER.operating_profit':'C63',
          'ER.profit_before_tax':'C68','ER.tax':'C69','ER.net_profit':'C70',
          'ECPN.capital':'F53','ECPN.reserve':'G53','ECPN.retained':'H53',
          'EFE.AO':'F71','EFE.AI':'F75','EFE.AF':'F82','EFE.final':'F88',
          'balances.cash':'C96','balances.inventory':'C100','balances.tax_payable':'E96',
          'balances.loan_cp':'E99','balances.loan_lp':'E108','balances.interest_payable':'E100'}
    for key,cell in refs.items():
        group,line=key.split('.')
        expected=Decimal(str(source[cell]['value']))
        actual=result[group][line]
        if key in ('ER.cost','ER.tax'): expected=abs(expected)
        assert abs(actual-expected)<Decimal('.000001'),key
    assert all(result['checks'].values())
    assert result['balances']['dividends_payable']==Decimal('.15')
    assert abs(result['ESF']['assets']-Decimal('841395.6666666666666666666667'))<Decimal('.000001')
    assert source['L83']['value']=='#REF!'
    assert source['L85']['value']=='#REF!'


def test_changing_sale_propagates_to_all_statements_and_preserves_identity():
    ledger=park_city();before=project(ledger)
    apply_operation(ledger,{'type':'sale','amount':'1000','cash_part':'1000','cost':'400'})
    after=project(ledger)
    assert after['ER']['net_profit']-before['ER']['net_profit']==Decimal('423')
    assert after['EFE']['final']-before['EFE']['final']==1000
    assert after['ECPN']['total']-before['ECPN']['total']==423
    assert after['ESF']['assets']-before['ESF']['assets']==600
    assert after['ESF']['liabilities']-before['ESF']['liabilities']==177
    assert all(after['checks'].values())


def test_pd4_incomplete_efe_cannot_be_accepted_as_a_reconciled_golden():
    b=json.loads((ROOT/'docs/evidence/FC PD4 26-2 Soluciónvf.json').read_text(encoding='utf-8'))['sheets']['Pregunta 2- sol']
    assert Decimal(str(b['P44']['value']))+Decimal(str(b['P45']['value']))!=Decimal(str(b['P46']['value']))
    # Missing sale receipt inferred by reconciliation, not a new official golden.
    assert Decimal(str(b['P46']['value']))-Decimal(str(b['P45']['value']))-Decimal(str(b['P44']['value']))==278812
    assert abs(Decimal(str(b['F23']['value']))-Decimal(str(b['C23']['value']))-Decimal('.30'))<Decimal('.000001')

