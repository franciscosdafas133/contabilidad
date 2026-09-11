from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4
from decimal import Decimal
import json
import pytest
from fastapi.testclient import TestClient
from api.app import create_app
from engine.catalog import ROOT
from engine.exercises import get_exercise, solve
from engine.money import display


@pytest.fixture
def client(tmp_path):
    return TestClient(create_app(tmp_path/'progress.sqlite3'))


def payload(answers,mode='practice'):
    return {'attempt_id':str(uuid4()),'mode':mode,'answers':answers,'elapsed_seconds':12}


def correct_answers(id):
    ex=get_exercise(id);solution=solve(ex)
    return {task['id']:solution[task['id']] if task['type']=='choice' else display(solution.get(task['id'],0)) for task in ex['tasks']}


def test_health_and_no_exam_or_expected_leak(client):
    assert client.get('/api/health').json()['engine']=='deterministic'
    exercises=client.get('/api/exercises').json()
    assert len(exercises)==12
    assert all('pc1' not in ex['id'] for ex in exercises)
    assert client.get('/api/exercises/pc1_p2').status_code==404
    for ex in exercises:
        data=client.get('/api/exercises/'+ex['id']).json()
        assert 'expected' not in data and 'solution' not in data
        if data['kind']=='efe': assert all('activity' not in row for row in data['data']['flows'])


@pytest.mark.parametrize('id',['pd1_clasificacion','semana1_caso1','pd1_ecuacion','pd2_esf','pd3_er','pd3_ecpn','pd3_efe','pd4_terracan','poder_er','las_vegas_er','las_vegas_efe','valparaiso_ecpn'])
def test_complete_each_public_exercise_and_compare_source(client,id):
    ex=get_exercise(id)
    fixture=json.loads((ROOT/f'tests/fixtures/{id}.json').read_text(encoding='utf-8'))
    answers=correct_answers(id)
    for key,value in fixture['expected'].items():
        if fixture['kind']=='classification': assert answers[key]==value
        # Compare unrounded values separately: Excel binary artifacts may lie at a cent tie.
        else: assert abs(Decimal(value)-solve(ex).get(key,Decimal(0)))<Decimal('.000001')
    result=client.post(f'/api/exercises/{id}/check',json=payload(answers))
    assert result.status_code==200,result.text
    assert result.json()['completed']
    assert client.get('/api/progress').json()['attempts'][0]['completed']


def test_partial_blank_and_sign_feedback_are_not_success(client):
    response=client.post('/api/exercises/pd3_efe/check',json=payload({'AI':'8000','AO':'NaN','flow_0':'AI'})).json()
    errors={f['id']:f['error_type'] for f in response['feedback']}
    assert errors['AI']=='sign'
    assert errors['AO']=='invalid'
    assert errors['flow_0']=='efe'
    assert errors['final']=='missing'
    assert not response['completed']
    assert all(f['rule_id'] and f['source'] for f in response['feedback'])


def test_storage_is_idempotent_and_survives_app_restart(tmp_path):
    path=tmp_path/'persist.sqlite3';client=TestClient(create_app(path))
    body=payload({'net_sales':'1'})
    first=client.post('/api/exercises/pd3_er/check',json=body)
    again=client.post('/api/exercises/pd3_er/check',json=body)
    assert first.json()==again.json()
    restarted=TestClient(create_app(path))
    report=restarted.get('/api/progress').json()
    assert len(report['attempts'])==1
    assert report['skills']['er']['total']==6
    assert report['recommendations']
    body['answers']['net_sales']='2'
    assert restarted.post('/api/exercises/pd3_er/check',json=body).status_code==409


def test_concurrent_progress_writes_are_preserved(client):
    with ThreadPoolExecutor(max_workers=4) as pool:
        results=list(pool.map(lambda _:client.post('/api/exercises/pd3_er/check',json=payload({})).status_code,range(8)))
    assert results==[200]*8
    assert len(client.get('/api/progress').json()['attempts'])==8


def test_malformed_requests_unknown_answers_and_origin(client):
    assert client.post('/api/exercises/pd3_er/check',json={}).status_code==422
    assert client.post('/api/exercises/pd3_er/check',json=payload({'unknown':'5'})).status_code==422
    assert client.post('/api/exercises/pd3_er/check',json=payload({'tax':2986.875})).status_code==422
    assert client.post('/api/exercises/pd3_er/check',json=payload({}),headers={'Origin':'https://evil.example'}).status_code==403
    assert client.get('/api/health',headers={'Host':'evil.example'}).status_code==400
    invalid=payload({});invalid['attempt_id']='x'*36
    assert client.post('/api/exercises/pd3_er/check',json=invalid).status_code==422


def test_simulator_replays_typed_operations_and_rejects_free_edits(client):
    operations=[{'type':'contribution','amount':'1000'},{'type':'purchase','amount':'100','cash_part':'100'},
                {'type':'sale','amount':'150','cash_part':'150','cost':'100'}]
    body={'scenario':'empty','operations':operations}
    a=client.post('/api/simulate',json=body)
    assert a.status_code==200,a.text
    assert a.json()==client.post('/api/simulate',json=body).json()
    result=a.json()
    assert result['after']['ER']['net_profit']=='35.25'
    assert result['after']['EFE']['final']=='1050.00'
    assert all(result['after']['checks'].values())
    assert any(row['account']=='tax_payable' and row['origin']=='recalculated' for row in result['changes'])
    body['operations'].append({'type':'sale','amount':'10','cash_part':'10','cost':'100'})
    assert client.post('/api/simulate',json=body).status_code==422
    assert client.post('/api/simulate',json={'balances':{'cash':'9'}}).status_code==422


def test_park_city_api_has_trace_and_invariants(client):
    result=client.post('/api/simulate',json={'scenario':'park_city','operations':[]}).json()
    assert result['after']['ER']['net_profit']=='188141.00'
    assert result['after']['ESF']['assets']=='841395.67'
    assert all(result['after']['checks'].values())
    assert all(t['rule_id'] and t['source'] for t in result['after']['trace'])


def test_no_llm_calls_in_runtime_source():
    forbidden=['import openai','from openai','anthropic','api.openai.com','chat.completions']
    for folder in ('engine','api'):
        for path in (ROOT/folder).glob('*.py'):
            content=path.read_text(encoding='utf-8')
            assert not any(term in content for term in forbidden)
