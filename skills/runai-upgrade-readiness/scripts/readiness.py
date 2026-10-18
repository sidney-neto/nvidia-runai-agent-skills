#!/usr/bin/env python3
"""Offline bounded profile selection and upgrade planning; never executes changes."""
import argparse
from datetime import datetime
import json
from pathlib import Path
import re


def release(raw):
    if not isinstance(raw,str): return None
    match=re.fullmatch(r'v?(0|[1-9]\d*)\.(0|[1-9]\d*)(?:\.(0|[1-9]\d*))?',raw)
    return '.'.join(str(int(part or 0)) for part in match.groups()) if match else None


def select(environment, rules, workflow):
    local=environment.get('local_profile')
    candidates=[p for p in rules['profiles'] if p['workflow']==workflow and p['deployment']==environment['deployment']]
    if local and local.get('scope')==environment.get('scope') and local.get('workflow',workflow)==workflow and local.get('component') in {p['component'] for p in candidates}:
        if not all(local.get(key) for key in ('component','provenance','scope','captured_at')):
            return {'state':'missing-evidence','reason':'local provenance incomplete'}
        observed=environment.get('components',{}).get(local['component'],{}).get('raw_version')
        declared=local.get('raw_version')
        if observed!=declared and not (release(observed) and release(observed)==release(declared)):
            return {'state':'conflict','reason':'local declaration contradicts observed version'}
    matches=[]
    for profile in candidates:
        raw=environment.get('components',{}).get(profile['component'],{}).get('raw_version')
        if profile.get('provenance_type')=='local':
            if not all(profile.get(k) for k in ('scope','provenance','captured_at','exact_raw')):continue
            try: datetime.fromisoformat(profile['captured_at'].replace('Z','+00:00'))
            except ValueError: continue
            if raw==profile['exact_raw'] and environment.get('scope')==profile['scope']:matches.append(profile)
        elif release(raw) in profile['versions']:matches.append(profile)
    if len(matches)>1:return {'state':'conflict','reason':'multiple applicable profiles; resolve evidence conflict'}
    if not matches:return {'state':'missing-evidence','reason':'No bounded profile matches; continue version-independent offline analysis.'}
    profile=matches[0]
    if not environment.get('workload_type'):
        return {'state':'missing-evidence','reason':'workload/submission path missing'}
    if environment['workload_type'] not in profile['workload_types']:
        return {'state':'incompatible','reason':'profile does not cover this workload/submission path'}
    missing_settings=[s for s in profile['settings'] if environment.get('settings',{}).get(s) is not True]
    if missing_settings:return {'state':'missing-evidence','settings':missing_settings}
    for capability in profile['required_capabilities']:
        cap=environment.get('capabilities',{}).get(capability)
        if cap is None:return {'state':'missing-evidence','capability':capability}
        if cap.get('state')!='available':return {'state':cap.get('state','unverified'),'capability':capability}
        if cap.get('permitted') is False:return {'state':'permission-denied','capability':capability}
        if not all(cap.get(key) is True for key in ('advertised','usable','permitted')):
            return {'state':'unverified','capability':capability}
    return {'state':'local-procedure' if profile.get('provenance_type')=='local' else 'documented-procedure','profile':profile,'observed_component':profile['component'],
            'vendor_supported':None,'authorization':'Not granted by this result; apply existing exact-scope user authorization and server RBAC.'}


def plan(data, rules):
    current,target=release(data.get('current')),release(data.get('target'))
    matches=[t for t in rules['transitions'] if t['current']==current and t['target']==target and t['deployment']==data.get('deployment')]
    if len(matches)>1:return {'state':'conflict','reason':'multiple transitions'}
    if not matches:return {'state':'missing-evidence','current_raw':data.get('current'),'target_raw':data.get('target'),'reason':'No reviewed transition. Do not infer upgrade distance or intermediate releases.'}
    transition=matches[0]
    observed=data.get('components',{})
    for name in ('runai-control-plane','runai-cluster'):
        component=observed.get(name,{})
        if not release(component.get('raw_version')) or not component.get('origin'):
            return {'state':'missing-evidence','reason':'Independent control-plane and cluster version provenance required.'}
    cluster=release(observed['runai-cluster']['raw_version'])
    control_plane=release(observed['runai-control-plane']['raw_version'])
    if cluster!=current:return {'state':'conflict','reason':'Requested current version contradicts observed cluster.'}
    if control_plane not in (current,target):
        return {'state':'missing-evidence','reason':'Mixed control-plane/cluster transition is not covered by this profile.'}
    if data.get('edition') not in transition['editions']:return {'state':'missing-evidence','reason':'edition/support model unresolved'}
    kubernetes=release(data.get('kubernetes'))
    if not kubernetes:return {'state':'missing-evidence','reason':'Kubernetes version ambiguous'}
    major,minor,_=map(int,kubernetes.split('.'))
    if major!=transition['kubernetes_major'] or minor not in transition['kubernetes_minor_overlap']:
        return {'state':'incompatible','reason':'No current/target Kubernetes overlap in this reviewed plan. Independently plan an infrastructure transition.'}
    required=list(transition['prerequisites'])
    if data.get('fractions') is True:required+=transition['fraction_prerequisites']
    elif data.get('fractions') is not False:return {'state':'missing-evidence','reason':'fraction workload inventory missing'}
    if data['edition']=='support-entitled':required.append('entitlement_verified')
    missing=[key for key in required if data.get('prerequisites',{}).get(key) is not True]
    stages=[stage for stage in transition['stages'] if not (stage=='control-plane' and control_plane==target)]
    return {'state':'missing-prerequisites' if missing else 'documented-plan','missing':missing,'stages':stages,
            'sources':transition['sources'],'vendor_supported':None,
            'limitations':['This is a plan, not authorization or a live compatibility certificate.','Every stage must succeed before the next; recheck all node versions and exact distribution support.','Helm rollback does not reverse database/CRD migrations or restore persistent data.','Recover fractional workloads only after verifying manifests, credentials, model assets and retained volumes.']}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input');parser.add_argument('--workflow',default='fraction-limit');parser.add_argument('--upgrade',action='store_true')
    parser.add_argument('--profiles',type=Path,default=Path(__file__).resolve().parents[1]/'references/profiles.json')
    args=parser.parse_args()
    try:
        path=Path(args.input)
        if path.stat().st_size>2_000_000 or args.profiles.stat().st_size>2_000_000:raise ValueError('input too large')
        data=json.loads(path.read_text());rules=json.loads(args.profiles.read_text())
        result=plan(data,rules) if args.upgrade else select(data,rules,args.workflow)
        print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))
        return 0 if result['state'] in ('documented-plan','documented-procedure','local-procedure') else 2
    except (ValueError,KeyError,TypeError,OSError):parser.exit(2,'Invalid readiness input; no input values echoed.\n')

if __name__=='__main__':raise SystemExit(main())
