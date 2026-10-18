#!/usr/bin/env python3
"""Offline health summary from local snapshot v1; no live adapters."""
def analyze(data):
    findings = []
    cp = [n for n in data['nodes'] if n['control_plane']]
    if len(cp) == 1: findings.append('single_control_plane_no_ha_assumption')
    if not cp: findings.append('control_plane_inventory_missing')
    for node in data['nodes']:
        if node['ready'] is not True: findings.append('node_not_confirmed_ready:' + node['name'])
    versions = {}
    for component in data['components']:
        versions.setdefault(component['name'], []).append({'raw_version': component['raw_version'], 'origin': component['origin'], 'node': component.get('node')})
    for condition in data.get('conditions', []):
        if condition['state'] != 'healthy': findings.append(condition['state'] + ':' + condition['component'])
    pages = data['pagination']
    if not pages['complete'] or (pages['expected_pages'] is not None and pages['pages'] != pages['expected_pages']):
        findings.append('partial_inventory')
    return {'captured_at': data['captured_at'], 'target': data['target'], 'findings': findings, 'versions': versions,
            'uncertainty': 'Node readiness does not prove control-plane connectivity, scheduler health, or vendor compatibility.',
            'next_action': 'Correlate named controller conditions and bounded events at the same timestamp.'}

import argparse
import json
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    args = parser.parse_args()
    try:
        path = Path(args.input)
        if path.stat().st_size > 2_000_000: raise ValueError('input too large')
        result = analyze(json.loads(path.read_text()))
        print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    except (ValueError, KeyError, TypeError, OSError):
        parser.exit(2, 'Invalid or incomplete offline input; no input values echoed.\n')

if __name__ == '__main__': main()
