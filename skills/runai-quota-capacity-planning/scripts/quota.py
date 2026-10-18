#!/usr/bin/env python3
"""Offline accounting of local snapshot v1; no Run:ai API mapping is implied."""
import argparse
import json
import math
from pathlib import Path


def number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
        raise ValueError('expected finite nonnegative GPU-equivalent quantity')
    return value


def calculate(data):
    pools = {}
    seen_nodes, seen_quotas = set(), set()
    for node in data['nodes']:
        if node['name'] in seen_nodes:
            raise ValueError('duplicate node; merge pagination before accounting')
        seen_nodes.add(node['name'])
        if not node['physical_gpus']:
            continue
        key = (data['target']['cluster'], node['node_pool'], node['gpu_type'])
        p = pools.setdefault(key, {'physical_gpus': 0, 'allocatable_gpu_equivalents': 0, 'projects': [], 'departments': []})
        p['physical_gpus'] += number(node['physical_gpus'])
        p['allocatable_gpu_equivalents'] += number(node['allocatable_gpu_equivalents'])
    for quota in data['quotas']:
        key = (data['target']['cluster'], quota['node_pool'], quota['gpu_type'])
        unique = (*key, quota['scope'], quota['id'])
        if unique in seen_quotas:
            raise ValueError('duplicate quota; merge pagination before accounting')
        seen_quotas.add(unique)
        if quota['quota'] not in (None, 'unlimited'):
            number(quota['quota'])
        if quota['allocated'] is not None:
            number(quota['allocated'])
        p = pools.setdefault(key, {'physical_gpus': None, 'allocatable_gpu_equivalents': None, 'projects': [], 'departments': []})
        if quota['scope'] not in ('project', 'department'):
            raise ValueError('unknown quota scope')
        p[quota['scope'] + 's'].append(quota)
    output = []
    pagination = data['pagination']
    complete = pagination['complete'] and (pagination['expected_pages'] is None or pagination['pages'] == pagination['expected_pages'])
    for (cluster, pool, gpu), p in sorted(pools.items(), key=lambda item: str(item[0])):
        projects, departments = p.pop('projects'), p.pop('departments')
        finite = [q for q in projects if q['quota'] not in (None, 'unlimited')]
        total = sum(q['quota'] for q in finite)
        p.update(cluster=cluster, node_pool=pool, gpu_type=gpu, finite_project_quota=total,
                 finite_department_quota=sum(q['quota'] for q in departments if q['quota'] not in (None, 'unlimited')),
                 unlimited_projects=sorted(q['id'] for q in projects if q['quota'] == 'unlimited'),
                 unknown_projects=sorted(q['id'] for q in projects if q['quota'] is None),
                 allocated_project_gpu_equivalents=sum(q['allocated'] for q in projects if q['allocated'] is not None),
                 allocation_total_complete=complete and all(q['allocated'] is not None for q in projects),
                 quota_total_complete=complete and len(finite) == len(projects),
                 capacity_complete=complete and pool is not None and gpu is not None and p['physical_gpus'] is not None,
                 over_quota_projects=sorted(q['id'] for q in finite if q['allocated'] is not None and q['allocated'] > q['quota']))
        p['configured_oversubscription'] = None
        if p['capacity_complete']:
            if total > p['allocatable_gpu_equivalents']:
                p['configured_oversubscription'] = True
            elif p['quota_total_complete']:
                p['configured_oversubscription'] = False
        output.append(p)
    return {'captured_at': data['captured_at'], 'partial': not complete, 'pools': output,
            'limitations': ['Quotas are entitlements, not measured compute activity.', 'Aggregate free capacity does not establish device fit.', 'Department totals are separate from project demand.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('snapshot'); parser.add_argument('--format', choices=['json','text'], default='json')
    args = parser.parse_args()
    try:
        if Path(args.snapshot).stat().st_size > 2_000_000: raise ValueError('input too large')
        report = calculate(json.loads(Path(args.snapshot).read_text()))
        if args.format == 'json': print(json.dumps(report, indent=2, sort_keys=True, allow_nan=False))
        else:
            for pool in report['pools']:
                print(f"{pool['cluster']}/{pool['node_pool']}/{pool['gpu_type']}: physical={pool['physical_gpus']}; finite project quotas={pool['finite_project_quota']}; department quotas={pool['finite_department_quota']}; configured oversubscription={pool['configured_oversubscription']}; over-quota projects={','.join(pool['over_quota_projects']) or 'none'}")
            print('Partial:', report['partial'])
    except (ValueError, KeyError, TypeError, OSError): parser.exit(2, 'Invalid or incomplete local snapshot; no input values echoed.\n')

if __name__ == '__main__': main()
