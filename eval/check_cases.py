#!/usr/bin/env python3
"""Replay the published model outputs. No provider calls; no keyword grading."""
import ast
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def function(code, name):
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.Global, ast.Nonlocal)):
            raise AssertionError('Unexpected external capability in evaluated code')
        if isinstance(node, ast.Attribute) and node.attr.startswith('_'):
            raise AssertionError('Unexpected private attribute')
        if isinstance(node, ast.Name) and node.id.startswith('__'):
            raise AssertionError('Unexpected private name')
    namespace = {'__builtins__': {'int': int, 'str': str, 'ValueError': ValueError, 'set': set, 'list': list, 'dict': dict, 'all': all, 'any': any, 'len': len, 'ord': ord, 'isinstance': isinstance}}
    exec(compile(tree, '<published model response>', 'exec'), namespace)
    return namespace[name]

rows = json.loads((ROOT / 'results.json').read_text())
assert {(r['model'], r['condition']) for r in rows} == {(m,c) for m in ('Fable 5.1','GPT-6 Astra') for c in ('baseline','skill')}
assert len(rows) == 4
for row in rows:
    tasks = {r['id']: r for r in row['response']['results']}
    assert set(tasks) == {'port','dedupe','stop'}
    parse = function(tasks['port']['code'], 'parse_port')
    for raw, expected in [(None,3000),('',3000),(' \t\n',3000),('1',1),('65535',65535),(' 0080 ',80),('3000',3000)]:
        assert parse(raw) == expected, (row['model'], row['condition'], raw)
    for raw in ['0','65536','-1','+80','8.0','1_000','80x','8 0','１２','٢','²']:
        try:
            parse(raw)
        except ValueError:
            pass
        else:
            raise AssertionError(('Expected ValueError', row['model'],row['condition'],raw))
    # Post-run stress probe: Python's default int-string limit exposes a gap in both Fable outputs.
    try:
        long_zero_ok = parse('0' * 5000 + '80') == 80
    except ValueError:
        long_zero_ok = False
    print(f"STRESS {row['model']} / {row['condition']}: 5000 leading zeros => {'pass' if long_zero_ok else 'FAIL (documented)'}")
    unique = function(tasks['dedupe']['code'], 'unique_records')
    original = [{'id':'b','value':1},{'id':'a','value':2},{'id':'b','value':3},{'id':'','value':4},{'id':'','value':5}]
    before = copy.deepcopy(original)
    output = unique(original)
    assert output == [original[0],original[1],original[3]]
    assert len(output)==3 and all(a is b for a,b in zip(output,[original[0],original[1],original[3]]))
    assert original == before and unique([]) == []
    assert tasks['stop'].get('code', '') == ''
    print(f"PASS {row['model']} / {row['condition']}: port boundaries/ASCII/errors; first-record order/identity/no mutation")
print('Validation-plan and stopping judgments are reviewed manually; code replay does not prove autonomous behavior or savings.')
