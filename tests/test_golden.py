import json
from pathlib import Path
from decimal import Decimal
import pytest
from engine.catalog import accounts, ROOT
from engine.equation import Ledger
from engine.closes import depreciation, income_tax, legal_reserve
from engine.projections import er, efe, ecpn, esf

FIXTURES=[json.loads(p.read_text(encoding='utf-8')) for p in sorted((ROOT/'tests/fixtures').glob('*.json'))]


@pytest.mark.parametrize('fixture',FIXTURES,ids=lambda f:f['id'])
def test_golden_provenance(fixture):
    assert fixture['expected'] and fixture['expected_cells']
    assert set(fixture['expected'])==set(fixture['expected_cells'])
    evidence=next(json.loads(p.read_text(encoding='utf-8')) for p in (ROOT/'docs/evidence').glob('*.json')
                  if p.name!='source_hashes.json' and json.loads(p.read_text(encoding='utf-8'))['sha256']==fixture['sha256'])
    for key,cell in fixture['expected_cells'].items():
        original=evidence['sheets'][fixture['sheet']][cell]['value']
        assert original is not None and original not in ('#REF!','#VALUE!')
        if fixture['kind']!='classification':
            assert abs(abs(Decimal(str(original)))-abs(Decimal(fixture['expected'][key])))<=Decimal(fixture['tolerance'])


def run_fixture(f):
    data=f['input'];kind=f['kind']
    if kind=='classification': return {k:accounts()[k]['element'] for k in data['accounts']}
    if kind=='depreciation': return {'amount':depreciation(**data)}
    if kind=='er': return er(**data)
    if kind=='efe': return efe(**data)
    if kind=='ecpn': return ecpn(**data)
    if kind=='close':
        profit=sum(map(Decimal,data['profit_items']));tax=income_tax(profit)
        reserve=legal_reserve(profit-tax,data['capital'])
        return {'tax':tax,'reserve':reserve,'retained':profit-tax-reserve}
    if kind=='matrix':
        ledger=Ledger(data['opening'])
        initial_profit=ledger.balances.get('retained',Decimal(0))
        for row in data['rows']:
            # This suite checks matrix balances only. AO here is a bookkeeping tag,
            # never used as golden EFE classification. Separate suites test EFE.
            ledger.apply(row['deltas'],row['label'],cash_activity='AO' if row['deltas'].get('cash') else None)
        if data['closing']:
            profit=ledger.balances.get('retained',Decimal(0))-initial_profit
            tax=income_tax(profit,data['closing']['tax_rate'])
            reserve=legal_reserve(profit-tax,ledger.balances['capital'],ledger.balances.get('reserve',0))
            if tax: ledger.apply({'tax_payable':tax,'retained':-tax},'IR',rule_id='tax')
            if reserve: ledger.apply({'reserve':reserve,'retained':-reserve},'RL',rule_id='reserve')
        report=esf(ledger.balances)
        assert report['balanced']
        return ledger.balances
    raise AssertionError(kind)


@pytest.mark.parametrize('fixture',FIXTURES,ids=lambda f:f['id'])
def test_golden(fixture):
    actual=run_fixture(fixture)
    for key,expected in fixture['expected'].items():
        if fixture['kind']=='classification': assert actual[key]==expected
        else: assert abs(actual.get(key,Decimal(0))-Decimal(expected))<=Decimal(fixture['tolerance']), f"{fixture['id']} {key}: {actual.get(key)} != {expected}"
