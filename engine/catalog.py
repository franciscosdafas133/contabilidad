import json
from pathlib import Path
from .money import AccountingError

ROOT = Path(__file__).resolve().parents[1]


def read_knowledge(name):
    return json.loads((ROOT / 'knowledge' / f'{name}.json').read_text(encoding='utf-8'))


def accounts():
    return {a['id']: a for a in read_knowledge('accounts')}


def account(key):
    try:
        return accounts()[key]
    except KeyError:
        raise AccountingError(f'Cuenta desconocida: {key}') from None


def trace(rule_id, inputs, output, lines):
    rule = read_knowledge('rules')[rule_id]
    return {'rule_id': rule_id, 'message': rule['text'], 'source': rule['source'],
            'inputs': inputs, 'output': output, 'statement_lines': lines}

