import hashlib
import json
from engine.catalog import ROOT, read_knowledge


def test_catalog_is_auditable_and_has_no_duplicate_ids():
    catalog = read_knowledge('accounts')
    assert len({a['id'] for a in catalog}) == len(catalog)
    for a in catalog:
        assert a['source'] and a['evidence'] in ('R','I','P')
        assert a['element'] in ('Activo','Pasivo','Patrimonio Neto','Ingreso','Gasto')
        assert a['natural_sign'] == (-1 if a['contra'] else 1)
    assert next(a for a in catalog if a['id']=='customer_advance')['element']=='Pasivo'


def test_original_corpus_was_not_modified():
    hashes=json.loads((ROOT/'docs/evidence/source_hashes.json').read_text(encoding='utf-8'))
    assert len(hashes)==49
    for name,digest in hashes.items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest, name


def test_all_rules_have_evidence():
    for rule in read_knowledge('rules').values():
        assert rule['source'] and rule['text']

