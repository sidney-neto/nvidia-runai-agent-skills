#!/usr/bin/env python3
"""Offline necessary device-fit check; not a scheduler simulator."""
import math

def analyze(data):
    request = data['pending_request']
    amount = request['gpu_equivalents']
    if isinstance(amount, bool) or not isinstance(amount, (int, float)) or not math.isfinite(amount) or not 0 < amount <= 1:
        raise ValueError('single-device analysis requires 0 < GPU equivalents <= 1')
    nodes = [n for n in data['nodes'] if n['node_pool'] == request['node_pool'] and n['gpu_type'] == request['gpu_type']]
    free = [value for node in nodes for value in node['free_device_gpu_equivalents']]
    if any(isinstance(v, bool) or not isinstance(v, (int,float)) or not math.isfinite(v) or not 0 <= v <= 1 for v in free):
        raise ValueError('invalid per-device free quantity')
    aggregate = sum(free) >= amount
    fit = any(v >= amount for v in free)
    pages = data['pagination']
    complete = pages['complete'] and (pages['expected_pages'] is None or pages['pages'] == pages['expected_pages'])
    if not complete and not fit: fit = None
    if not complete and not aggregate: aggregate = None
    return {'captured_at': data['captured_at'], 'aggregate_sufficient': aggregate, 'single_device_fit': fit,
            'findings': ['fragmentation'] if aggregate and fit is False else [],
            'complete': complete,
            'uncertainty': 'Necessary fit only. Quota, permission, CPU/memory, affinity, taints, gang and topology constraints remain untested.'}

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
