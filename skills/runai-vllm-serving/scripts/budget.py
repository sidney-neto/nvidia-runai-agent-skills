#!/usr/bin/env python3
"""Offline full-context KV budget estimate from evidenced per-GPU measurements."""
import math

def analyze(data):
    keys = ('max_model_len','max_num_seqs','kv_bytes_per_token_per_gpu','available_kv_bytes_per_gpu')
    for key in keys:
        value = data[key]
        if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or value <= 0:
            raise ValueError('budget inputs must be finite positive quantities')
    if any(int(data[k]) != data[k] for k in ('max_model_len','max_num_seqs')): raise ValueError('token/sequence counts must be integers')
    per_sequence = data['max_model_len'] * data['kv_bytes_per_token_per_gpu']
    capacity = int(data['available_kv_bytes_per_gpu'] // per_sequence)
    return {'state': 'inconsistent_full_concurrency_budget' if capacity < data['max_num_seqs'] else 'fits_kv_budget_only',
            'full_length_sequence_capacity': capacity,
            'required_kv_bytes_per_gpu': per_sequence * data['max_num_seqs'],
            'uncertainty': 'Worst-case full-length resident sequences. Prefix reuse, chunking and scheduler preemption can change residency; this does not prove launch failure.',
            'next_action': 'Verify installed-version flags, model KV geometry/TP partitioning, weights, activation/workspace headroom, and measured free KV budget. Benchmark only within authorized resource scope.'}

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
