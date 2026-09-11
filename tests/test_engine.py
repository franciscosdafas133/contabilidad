from copy import deepcopy
from decimal import Decimal
import pytest
from engine.money import AccountingError, number, display
from engine.closes import depreciation, amortization, legal_reserve, income_tax, prorate, periodic_cost
from engine.equation import Ledger
from engine.transactions import apply_operation
from engine.projections import project, esf
from engine.scenarios import equation_case1


@pytest.mark.parametrize('value',['NaN','Infinity','-Infinity',True,1.2,'1,000','', '1e16','0.00000000000000000000000000001'])
def test_rejects_invalid_decimal(value):
    with pytest.raises(AccountingError): number(value)


def test_decimal_tie_rounding_and_fractional_source_precision():
    assert display('2986.875')=='2986.88'
    assert display('-2986.875')=='-2986.88'
    assert income_tax('10125')==Decimal('2986.875')


@pytest.mark.parametrize('profit,capital,current,expected',[
    ('10000','10000','1500','500'),('10000','10000','2000','0'),
    ('10000','10000','2500','0'),('-5000','10000','0','0'),('10000','10000','0','1000')])
def test_reserve_boundaries(profit,capital,current,expected):
    assert legal_reserve(profit,capital,current)==Decimal(expected)


def test_depreciation_land_rescue_life_and_proration():
    assert depreciation('250000','0','0','12',land=True)==0
    assert depreciation('10000','1000','5','120')==9000
    assert depreciation('10000','1000','5','12',accumulated='8500')==500
    assert amortization('20000','4','1')==Decimal('20000')/48
    assert prorate('48000','6','48')==6000
    with pytest.raises(AccountingError): depreciation('100','110','5','1')
    with pytest.raises(AccountingError): depreciation('100','0','0','1')
    with pytest.raises(AccountingError): prorate('48000','49','48')


def test_periodic_theft_is_not_counted_twice():
    assert periodic_cost('25000','150000','35000','10000','1000','6000')==143000
    assert periodic_cost('25000','150000','35000','10000','1000','6000','cost')==149000
    with pytest.raises(AccountingError): periodic_cost('0','10','11')
    with pytest.raises(AccountingError): periodic_cost('0','10','0',theft_policy='guess')


def test_typical_case1_from_operations_matches_independent_golden():
    result=project(equation_case1(),close=False,reserve=False)
    assert result['ER']['net_profit']==9900
    assert result['ESF']['assets']==300100
    assert result['balances']['cash']==248100
    assert result['balances']['inventory']==10000
    assert all(result['checks'].values())


def test_project_is_pure_and_does_not_close_twice():
    ledger=equation_case1();before=deepcopy(ledger)
    assert project(ledger)==project(ledger)
    assert ledger==before
    assert all(project(ledger)['checks'].values())


def test_credit_sale_has_profit_without_cash_and_correct_cost():
    ledger=Ledger({'inventory':'100','capital':'100'})
    apply_operation(ledger,{'type':'sale','amount':'150','cash_part':'0','cost':'100'})
    report=project(ledger,close=False)
    assert report['ER']['net_profit']==50
    assert report['EFE']['change']==0
    assert report['balances']['receivables']==150
    assert report['ESF']['balanced']


def test_noncash_contributions_and_unpaid_dividends():
    ledger=Ledger({'cash':'100','retained':'100'})
    apply_operation(ledger,{'type':'asset_contribution','amount':'200'})
    apply_operation(ledger,{'type':'dividend','amount':'50'})
    report=project(ledger)
    assert report['EFE']['change']==0
    assert report['balances']['dividends_payable']==50
    apply_operation(ledger,{'type':'dividend_payment','amount':'20'})
    assert project(ledger)['EFE']['AF']==-20
    assert ledger.balances['dividends_payable']==30


def test_overdraft_reclassifies_without_changing_cash():
    ledger=Ledger({'cash':'-100','equipment':'300','capital':'200'})
    report=project(ledger)
    assert report['ESF']['assets']==300
    assert report['ESF']['liabilities']==100
    assert report['EFE']['final']==-100
    assert ledger.balances['cash']==-100
    assert report['ESF']['sections']['PC'][0]['id']=='overdraft'


@pytest.mark.parametrize('operation',[
    {'type':'sale','amount':'200','cash_part':'200','cost':'101'},
    {'type':'collection','amount':'1'},
    {'type':'purchase','amount':'20','cash_part':'21'},
    {'type':'contribution','amount':'-10'},
    {'type':'contribution','amount':'10','profit':'100'},
    {'type':'interest','amount':'10','cash_part':'1','activity':'AI'},
    {'type':'sale','amount':'1'},
    {'type':'unknown','amount':'10'},
])
def test_rejected_operations_are_atomic(operation):
    ledger=Ledger({'inventory':'100','capital':'100'});before=deepcopy(ledger)
    with pytest.raises(AccountingError): apply_operation(ledger,operation)
    assert ledger==before


def test_equation_rejects_missing_contra_unknown_and_unbalanced():
    for balances in ({'cash':'100'}, {'unknown':'0'}, {'cash':'100','dep_equipment':'1','capital':'101'}):
        with pytest.raises(AccountingError): Ledger(balances)
    ledger=Ledger()
    with pytest.raises(AccountingError): ledger.apply({'cash':'10','capital':'9'},'invalid',cash_activity='AF')
    with pytest.raises(AccountingError): ledger.apply({'cash':'10','capital':'10'},'missing classification')
    with pytest.raises(AccountingError): ledger.apply({'equipment':'10','capital':'10'},'noncash',cash_activity='AF')


def test_loss_does_not_create_tax_or_reserve():
    ledger=Ledger({'cash':'100','capital':'100'})
    apply_operation(ledger,{'type':'salary','amount':'10','cash_part':'10'})
    report=project(ledger)
    assert report['ER']['tax']==report['ECPN']['transfer']==0
    assert report['ER']['net_profit']==-10
    assert all(report['checks'].values())
